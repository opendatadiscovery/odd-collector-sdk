from pathlib import Path
from typing import Dict, Type, Union

from pyaml_env import parse_config

from .collector_config import CollectorConfig
from .plugin import Plugin
from ..logger import logger

class CollectorConfigLoader:
    def __init__(
        self, config_path: Union[str, Path], plugin_factory: Dict[str, Type[Plugin]]
    ) -> None:
        self.plugin_factory = plugin_factory
        self.path = Path(config_path).resolve()

    def load(self) -> CollectorConfig:
        logger.debug("Start reading config")
        parsed = parse_config(str(self.path))

        parsed["plugins"] = [
            self.plugin_factory[plugin["type"]].parse_obj(plugin)
            for plugin in parsed["plugins"]
        ]

        return CollectorConfig.parse_obj(parsed)
