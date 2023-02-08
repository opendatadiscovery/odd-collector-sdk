import os
from pathlib import Path
from typing import Dict, Type, Union

from pyaml_env import parse_config

from ..errors import LoadConfigError
from ..logger import logger
from .collector_config import CollectorConfig
from .plugin import Plugin


class CollectorConfigLoader:
    def __init__(
        self, config_path: Union[str, Path], plugin_factory: Dict[str, Type[Plugin]]
    ) -> None:
        self.plugin_factory = plugin_factory

        config_path = config_path or os.getenv("CONFIG_PATH", "collector_config.yaml")
        self.path = Path(config_path).resolve()

    def load(self) -> CollectorConfig:
        logger.debug(f"Config path {self.path}")
        logger.info("Start reading config")

        try:
            parsed = parse_config(str(self.path))
            parsed["plugins"] = [
                self.plugin_factory[plugin["type"]].parse_obj(plugin)
                for plugin in parsed["plugins"]
            ]

            return CollectorConfig.parse_obj(parsed)
        except Exception as e:
            raise LoadConfigError(e)
