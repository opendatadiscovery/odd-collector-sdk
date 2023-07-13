import json
from enum import Enum
from typing import Any, Optional

from flatdict import FlatDict
from odd_models.models import MetadataExtension

from odd_collector_sdk.utils.json_encoder import CustomJSONEncoder

prefix = "https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/extensions"


class DefinitionType(Enum):
    DATASET = "DataSetExtension"
    DATASET_FIELD = "DataSetFieldExtension"


def extract_metadata(
    datasource: str,
    entity: Any,
    definition: DefinitionType,
    jsonify: Optional[bool] = False,
) -> MetadataExtension:
    """
    :param datasource: name of datasource.
    :param entity: metadata entity.
    :param definition: definition type.
    :param jsonify: serialize metadata to display properly on UI.
    """
    schema_url = f"{prefix}/{datasource}.json#/definitions/{definition.value}"
    if hasattr(entity, "odd_metadata"):
        data = entity.odd_metadata
    else:
        data = entity.__dict__

    not_none = {}
    for key, value in data.items():
        if value:
            if isinstance(value, dict):
                value = str(FlatDict(value, delimiter="."))
            if jsonify and not isinstance(value, (str, int)):
                not_none[key] = json.dumps(value, cls=CustomJSONEncoder)
            else:
                not_none[key] = value
    return MetadataExtension(schema_url=schema_url, metadata=not_none)
