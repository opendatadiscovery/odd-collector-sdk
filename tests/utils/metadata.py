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


def test_extract_metadata_nested_dict():
    datasource = "example_datasource"
    entity = TestMetadata()
    entity.test_nested = {
        "name": "nested dict",
        "nested": {
            "key1": "value1",
            "key2": "value2"
        }
    }
    definition = DefinitionType.DATASET

    result = extract_metadata(datasource, entity, definition, jsonify=True)

    assert isinstance(result, MetadataExtension)
    assert result.schema_url == f"https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/extensions/{datasource}.json#/definitions/{definition.value}"
    result = {
        'test_float': '0.01',
        'test_uuid': json.dumps(str(entity.test_uuid)),
        'test_str': 'test',
        'test_nested.name': 'nested dict',
        'test_nested.nested.key1': 'value1',
        'test_nested.nested.key2': 'value2'
    }
    assert result == {'test_float': '0.01', "test_uuid": json.dumps(str(entity.test_uuid)), 'test_str': 'test',
                      'test_nested.name': 'nested dict', 'test_nested.nested.key1': 'value1',
                      'test_nested.nested.key2': 'value2'}


def test_extract_metadata_empty():
    datasource = "example_datasource"
    entity = TestMetadata()
    entity.odd_metadata = {}
    definition = DefinitionType.DATASET

    result = extract_metadata(datasource, entity, definition, jsonify=False)
    assert result.metadata == {}


def test_extract_metadata_with_none_values():
    datasource = "example_datasource"
    entity = TestMetadata()
    entity.test_float = None
    entity.test_uuid = None
    entity.test_str = None
    definition = DefinitionType.DATASET

    result = extract_metadata(datasource, entity, definition, jsonify=False)
    assert result.metadata == {}
