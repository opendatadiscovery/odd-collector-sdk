from abc import ABC, abstractmethod
from typing import NamedTuple, Union

from odd_models.models import DataEntityList

from odd_collector_sdk.domain.plugin import Plugin


class AbstractAdapter(ABC):
    @abstractmethod
    def get_data_source_oddrn(self) -> str:
        pass

    @abstractmethod
    def get_data_entity_list(self) -> DataEntityList:
        pass


class AsyncAbstractAdapter(ABC):
    @abstractmethod
    async def get_data_source_oddrn(self) -> str:
        pass

    @abstractmethod
    async def get_data_entity_list(self) -> DataEntityList:
        pass


AdapterConfig = Plugin


class Adapter(NamedTuple):
    adapter: Union[AbstractAdapter, AsyncAbstractAdapter]
    config: AdapterConfig
