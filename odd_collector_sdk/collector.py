from datetime import datetime
from typing import List

import tzlocal
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from odd_models.models import DataSource, DataSourceList

from odd_collector_sdk.domain.adapter import Adapter
from odd_collector_sdk.job import create_job
from odd_collector_sdk.types import PluginFactory

from .api.datasource_api import PlatformApi
from .api.http_client import HttpClient
from .domain.adapters_initializer import AdaptersInitializer
from .domain.collector_config import CollectorConfig
from .domain.collector_config_loader import CollectorConfigLoader
import logging


logging.getLogger("apscheduler.scheduler").setLevel(logging.ERROR)

class Collector:
    _adapters: List[Adapter]

    def __init__(
        self, config_path: str, root_package: str, plugin_factory: PluginFactory
    ) -> None:
        loader = CollectorConfigLoader(config_path, plugin_factory)
        self.config: CollectorConfig = loader.load()

        adapter_initializer = AdaptersInitializer(root_package, self.config.plugins)

        self._adapters = adapter_initializer.init_adapters()
        self._api = PlatformApi(
            http_client=HttpClient(
                token=self.config.token,
                connection_timeout_seconds=self.config.connection_timeout_seconds,
            ),
            platform_url=self.config.platform_host_url,
        )

    def start_polling(self):
        misfire_grace_time = (
            self.config.misfire_grace_time or self.config.default_pulling_interval * 60
        )

        scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))

        for adapter in self._adapters:
            scheduler.add_job(
                create_job(self._api, adapter, self.config.chunk_size).start,
                "interval",
                minutes=self.config.default_pulling_interval,
                next_run_time=datetime.now(),
                misfire_grace_time=misfire_grace_time,
                max_instances=self.config.max_instances,
                coalesce=True,
                id=adapter.config.name,
            )
        scheduler.start()

    async def register_data_sources(self):
        data_sources: List[DataSource] = [
            DataSource(
                oddrn=adapter.get_data_source_oddrn(),
                name=config.name,
                description=config.description,
            )
            for adapter, config in self._adapters
        ]

        request = DataSourceList(items=data_sources)

        async with ClientSession() as session:
            return await self._api.register_datasource(request, session)
