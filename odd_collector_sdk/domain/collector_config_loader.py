import logging
import pydantic

from typing import List

from .collector_config import CollectorConfig
from pyaml_env import parse_config


class CollectorConfigLoader:
    def __init__(self, config_path: str, plugins_union_type) -> None:
        self.union = plugins_union_type
        self.path = config_path
        pass

    def load(self) -> CollectorConfig:
        try:
            parsed = parse_config(self.path)
            model = pydantic.create_model(
                "DynamicModel",
                __base__=CollectorConfig,
                plugins=(List[self.union], ...),
            )
            return model.parse_obj(parsed)
        except Exception as e:
            logging.error(e)
