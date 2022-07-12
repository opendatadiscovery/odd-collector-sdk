import pydantic

from .plugin import Plugin
from typing import List


class CollectorConfig(pydantic.BaseSettings):
    default_pulling_interval: int
    token: str
    plugins: List[Plugin]
    platform_host_url: str
