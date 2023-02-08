from typing import List, Optional

import pydantic

from .plugin import Plugin


class CollectorConfig(pydantic.BaseSettings):
    default_pulling_interval: int
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
