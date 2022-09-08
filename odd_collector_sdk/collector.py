import asyncio

from asyncio import Task
from datetime import datetime
from functools import partial
from typing import List

import tzlocal
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from odd_models.models import DataSource, DataSourceList

from odd_collector_sdk.domain.adapter import AbstractAdapter
from odd_collector_sdk.types import PluginFactory

from .api.datasource_api import DataSourceApi
from .api.http_client import HttpClient
from .domain.adapters_initializer import AdaptersInitializer
from .domain.collector_config import CollectorConfig
from .domain.collector_config_loader import CollectorConfigLoader
from .logger import logger



class Collector:
    def __init__(
            self, config_path: str, root_package: str, plugin_factory: PluginFactory
    ) -> None:
        loader = CollectorConfigLoader(config_path, plugin_factory)
        self.config: CollectorConfig = loader.load()

        adapter_initializer = AdaptersInitializer(root_package, self.config.plugins)

        self.adapters_with_plugins = adapter_initializer.init_adapters()
        self.__api = DataSourceApi(
            http_client=HttpClient(token=self.config.token),
            platform_url=self.config.platform_host_url,
        )

    def start_polling(self):
        scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
        scheduler.add_job(
            self.__ingest_data,
            "interval",
            minutes=self.config.default_pulling_interval,
            next_run_time=datetime.now(),
        )
        scheduler.start()

    async def register_data_sources(self):
        data_sources: List[DataSource] = [
            DataSource(
                oddrn=adapter.get_data_source_oddrn(),
                name=plugin.name,
                description=plugin.description,
            )
            for adapter, plugin in self.adapters_with_plugins
        ]

        request = DataSourceList(items=data_sources)

        async with ClientSession() as session:
            return await self.__api.register_datasource(request, session)

    async def __do_tasks(self, tasks: List[Task]):
        finished, not_finished = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

        for task in finished:
            if task.exception():
                logger.error("Error", exc_info=task.exception())
                await self.__do_tasks(not_finished)

    async def __ingest_data(self):
        async with ClientSession() as session:
            send_request = partial(self.__send_request, session=session)
            tasks = [
                asyncio.create_task(send_request(adapter=adapter))
                for adapter, _ in self.adapters_with_plugins
            ]
            await self.__do_tasks(tasks)

    async def __get_data_entity_list(self, adapter: AbstractAdapter):
        result = adapter.get_data_entity_list()

        return await result if asyncio.iscoroutine(result) else result

    async def __send_request(self, adapter: AbstractAdapter, session: ClientSession):
        data_entity_list = await self.__get_data_entity_list(adapter)
        return await self.__api.ingest_data(data_entity_list, session)
