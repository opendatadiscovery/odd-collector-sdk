from typing import List
from pydantic import BaseModel
from . import DataSource


class RegisterDataSourceRequest(BaseModel):
    provider_oddrn: str
    items: List[DataSource]
