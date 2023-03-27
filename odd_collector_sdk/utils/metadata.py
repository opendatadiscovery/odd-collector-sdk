from enum import Enum
from typing import Any, Optional

from funcy import select

prefix = "https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/extensions"


class DefinitionType(Enum):
    DATASET = "DataSetExtension"
    DATASET_FIELD = "DataSetFieldExtension"


from odd_models.models import MetadataExtension


def extract_metadata(
    datasource: str,
    entity: Any,
    definition: DefinitionType,
    skip_keys: Optional[set] = None,
) -> MetadataExtension:
    schema_url = f"{prefix}/{datasource}.json#/definitions/{definition.value}"

    if hasattr(entity, "odd_metadata"):
        data = entity.odd_metadata
    else:
        data = entity.__dict__

    not_none = select(lambda x: x[1] is not None, data)

    return MetadataExtension(schema_url=schema_url, metadata=not_none)
