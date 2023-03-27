from enum import Enum
from typing import Any

from funcy import select

prefix = "https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/extensions/postgresql.json#/definitions"


class DefinitionType(Enum):
    DATASET = "DataSetExtension"
    DATASET_FIELD = "DataSetFieldExtension"


from odd_models.models import MetadataExtension


def extract_metadata(
    entity: Any, definition: DefinitionType, skip_keys: set = None
) -> MetadataExtension:
    schema_url = f"{prefix}/{definition.value}"

    if hasattr(entity, "odd_metadata"):
        data = entity.odd_metadata
    else:
        data = entity.__dict__

    not_none = select(lambda x: x[1] is not None, data)

    return MetadataExtension(schema_url=schema_url, metadata=not_none)
