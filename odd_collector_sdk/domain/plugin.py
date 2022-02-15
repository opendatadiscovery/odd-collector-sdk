from typing import Optional
import pydantic


class Plugin(pydantic.BaseSettings):
    name: str
    description: Optional[str] = None
    namespace: Optional[str] = None
