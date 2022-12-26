from typing import Dict, Type

from pyaml_env import parse_config

from .collector_config import CollectorConfig
from .plugin import Plugin


class CollectorConfigLoader:
    def __init__(
        self, config_path: str, plugin_factory: Dict[str, Type[Plugin]]
    ) -> None:
        self.plugin_factory = plugin_factory
        self.path = config_path

    def load(self) -> CollectorConfig:
        parsed = parse_config(self.path)

        parsed["plugins"] = [
            self.plugin_factory[plugin["type"]].parse_obj(plugin)
            for plugin in parsed["plugins"]
        ]

        return CollectorConfig.parse_obj(parsed)
