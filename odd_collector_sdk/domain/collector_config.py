import pydantic

from typing import Any


class CollectorConfig(pydantic.BaseSettings):
    default_pulling_interval: int
    token: str
    plugins: Any
    platform_host_url: str

    class Config:
        smart_union = True
