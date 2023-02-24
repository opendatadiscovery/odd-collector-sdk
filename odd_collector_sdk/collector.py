import asyncio
import logging
import signal
import traceback
from asyncio import AbstractEventLoop
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

import tzlocal
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from odd_models.models import DataSource, DataSourceList

from odd_collector_sdk.domain.adapter import Adapter
from odd_collector_sdk.job import create_job
from odd_collector_sdk.logger import logger
from odd_collector_sdk.shutdown import shutdown
from odd_collector_sdk.types import PluginFactory

from .api.datasource_api import PlatformApi
from .api.http_client import HttpClient
from .domain.adapters_initializer import AdaptersInitializer
from .domain.collector_config import CollectorConfig
from .domain.collector_config_loader import CollectorConfigLoader
from .utils.print_version import print_collector_packages_info, version

logging.getLogger("apscheduler.scheduler").setLevel(logging.ERROR)


class Collector:
    """All ODD collectors should use that class to run.

    Attributes:
        config_path: Path| str
            Path to "collector_config.yaml" file
        root_package: str
            Package name for derived collector
        plugin_factory: dict
            fabric for plugins
        plugins_package: str:
            subpackage where plugins are stored.

    Example:
        >>> collector = Collector(
            config_path=Path().cwd() / "collector_config.yaml",
            root_package="odd_collector",
            plugin_factory=PLUGIN_FACTORY,
        )
        >>>collector.run()

    """

    _adapters: List[Adapter]

    def __init__(
        self,
        config_path: Union[str, Path],
        root_package: str,
        plugin_factory: PluginFactory,
        plugins_package: str = "adapters",
    ) -> None:
        logger.success(f"Run {root_package}: {version(root_package)}")
        print_collector_packages_info(root_package)

        loader = CollectorConfigLoader(config_path, plugin_factory)
        self.config: CollectorConfig = loader.load()

        adapters_package = f"{root_package}.{plugins_package}"
        adapter_initializer = AdaptersInitializer(adapters_package, self.config.plugins)

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

    def run(self, loop: Optional[AbstractEventLoop] = None):
        try:
            if not loop:
                loop = asyncio.get_event_loop()

            signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
            for s in signals:
                loop.add_signal_handler(
                    s, lambda s=s: asyncio.create_task(shutdown(s, loop))
                )

            loop.run_until_complete(self.register_data_sources())

            self.start_polling()
            loop.run_forever()
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.error(e)
