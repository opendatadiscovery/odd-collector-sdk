import json

from dataclasses import dataclass
from uuid import UUID, uuid4

from odd_models.models import MetadataExtension

from odd_collector_sdk.utils.metadata import DefinitionType, extract_metadata


@dataclass
class TestMetadata:
    test_float: float = 0.01
    test_uuid: UUID = uuid4()
    test_str: str = 'test'


def test_extract_metadata():
    datasource = "example_datasource"
    entity = TestMetadata()
    definition = DefinitionType.DATASET

    result = extract_metadata(datasource, entity, definition, jsonify=False)

    assert isinstance(result, MetadataExtension)
    assert result.schema_url == f"https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/extensions/{datasource}.json#/definitions/{definition.value}"
    assert result.metadata == {"test_float": 0.01, "test_uuid": entity.test_uuid, "test_str": "test"}


def test_extract_metadata_serialized():
    datasource = "example_datasource"
    entity = TestMetadata()
    definition = DefinitionType.DATASET

    result = extract_metadata(datasource, entity, definition, jsonify=True)

    assert isinstance(result, MetadataExtension)
    assert result.schema_url == f"https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/extensions/{datasource}.json#/definitions/{definition.value}"
    assert result.metadata == {"test_float": "0.01", "test_uuid": json.dumps(str(entity.test_uuid)), "test_str": "test"}
