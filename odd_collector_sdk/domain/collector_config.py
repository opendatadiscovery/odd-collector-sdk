from typing import List, Optional

import pydantic

from .plugin import Plugin


class CollectorConfig(pydantic.BaseSettings):
    default_pulling_interval: int
    connection_timeout_seconds: int = 300
    token: str
    plugins: List[Plugin]
    platform_host_url: str
    chunk_size: Optional[int] = 250
