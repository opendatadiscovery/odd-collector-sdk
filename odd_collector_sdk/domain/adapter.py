from abc import ABC, abstractmethod
from typing import NamedTuple

from odd_models.models import DataEntityList

from odd_collector_sdk.domain.plugin import Plugin


class AbstractAdapter(ABC):
    @abstractmethod
    def get_data_source_oddrn(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_data_entity_list(self) -> DataEntityList:
        raise NotImplementedError()


AdapterConfig = Plugin


class Adapter(NamedTuple):
    adapter: AbstractAdapter
    config: AdapterConfig
