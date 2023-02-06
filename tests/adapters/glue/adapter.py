from odd_models.models import DataEntityList

from odd_collector_sdk.domain.adapter import AbstractAdapter
from .sub_pkg.sub_module import some_value

class Adapter(AbstractAdapter):
    def __init__(self, config: any) -> None:
        super().__init__()

    def get_data_entity_list(self) -> DataEntityList:
        return DataEntityList(data_source_oddrn="test")

    def get_data_source_oddrn(self) -> str:
        return "oddrn"
