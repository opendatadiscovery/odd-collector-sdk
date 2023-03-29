import os
from pathlib import Path
from typing import Dict, List, Optional, Type, Union

import pydantic
from pyaml_env import parse_config

from ..errors import LoadConfigError
from ..logger import logger
from .plugin import Plugin


class CollectorConfig(pydantic.BaseSettings):
    default_pulling_interval: Optional[int] = None  # minutes
    connection_timeout_seconds: int = 300
    token: str
    plugins: List[Plugin]
    platform_host_url: str
    chunk_size: int = 250
    misfire_grace_time: Optional[
        int
    ]  # seconds after the designated runtime that the job is still allowed to be run
    max_instances: Optional[
        int
    ] = 1  # maximum number of concurrently running instances allowed


def load_config(
    config_path: Union[str, Path], plugin_factory: Dict[str, Type[Plugin]]
) -> CollectorConfig:
    config_path = config_path or os.getenv("CONFIG_PATH", "collector_config.yaml")

    try:
        config_path = Path(config_path).resolve()
        logger.debug(f"{config_path=}")
        logger.info("Start reading config")

        parsed = parse_config(str(config_path))
        parsed["plugins"] = [
            plugin_factory[plugin["type"]].parse_obj(plugin)
            for plugin in parsed["plugins"]
        ]

        return CollectorConfig.parse_obj(parsed)
    except Exception as e:
        raise LoadConfigError(e)
