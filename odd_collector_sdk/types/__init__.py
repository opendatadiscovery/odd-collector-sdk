from typing import Type, Dict
from odd_collector_sdk.domain.plugin import Plugin


PluginFactory = Dict[str, Type[Plugin]]
