from typing_extensions import Literal

from odd_collector_sdk.domain.plugin import Plugin
from odd_collector_sdk.types import PluginFactory


class TestGluePlugin(Plugin):
    type: Literal["glue"]


class TestS3Plugin(Plugin):
    type: Literal["s3"]


PLUGIN_FACTORY: PluginFactory = {"glue": TestGluePlugin, "s3": TestS3Plugin}
