from typing import Union
from typing_extensions import Literal
from typing_extensions import Annotated

import pydantic
from odd_collector_sdk.domain.plugin import Plugin


class TestGluePlugin(Plugin):
    type: Literal["glue"]


class TestS3Plugin(Plugin):
    type: Literal["s3"]


AvailableTestPlugins = Annotated[
    Union[TestGluePlugin, TestS3Plugin],
    pydantic.Field(discriminator="type"),
]
