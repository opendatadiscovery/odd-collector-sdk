import yaml
import logging
import pydantic

from typing import List

from .collector_config import CollectorConfig


class CollectorConfigLoader:
    def __init__(self, config_path: str, plugins_union_type) -> None:
        self.union = plugins_union_type
        self.path = config_path
        pass

    def load(self) -> CollectorConfig:
        with open(self.path, "r") as stream:
            try:
                parsed_yaml_file = yaml.safe_load(stream)
                m = pydantic.create_model(
                    "DynamicModel",
                    __base__=CollectorConfig,
                    plugins=(List[self.union], ...),
                )
                res = m.parse_obj(parsed_yaml_file)

                return res
            except (yaml.YAMLError, pydantic.ValidationError) as e:
                logging.error(e)
