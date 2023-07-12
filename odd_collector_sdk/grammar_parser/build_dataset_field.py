from typing import Any
from pathlib import Path

from odd_models import DataSetField, DataSetFieldType, Type
from oddrn_generator import Generator
from odd_collector_sdk.grammar_parser.parser import FieldTypeMapper
from odd_collector_sdk.logger import logger
from odd_collector_sdk.grammar_parser.field_types import ParseType, StructType, ArrayType, MapType, BasicType, UnionType
from odd_collector_sdk.utils.metadata import DefinitionType, extract_metadata


class DatasetFieldBuilder:
    def __init__(self, data_source: str, oddrn_generator: Generator, parser_config_path: Path, odd_types_map: dict):
        self.data_source = data_source
        self.odd_types_map = odd_types_map
        self.oddrn_generator = oddrn_generator
        self.mapper = FieldTypeMapper(parser_config_path)

    def build_dataset_field(self, field: Any) -> list[DataSetField]:
        data_source = self.data_source
        oddrn_generator = self.oddrn_generator
        parser_input = str(field.type)
        logger.debug(f"Build dataset field for {field.name} with type {parser_input}")
        type_tree = self.mapper.parser.parse(parser_input)
        field_type = self.mapper.traverse_tree(type_tree)
        generated_dataset_fields = []

        def _build_ds_field_from_type(field_name: str, field_type: ParseType, parent_oddrn=None):
            if parent_oddrn is None:
                oddrn = oddrn_generator.get_oddrn_by_path("columns", field_name)
            else:
                oddrn = f"{parent_oddrn}/keys/{field_name}"

            if isinstance(field_type, StructType):
                generated_dataset_fields.append(
                    DataSetField(
                        oddrn=oddrn,
                        name=field_name,
                        metadata=[
                            extract_metadata(
                                data_source, field, DefinitionType.DATASET_FIELD
                            )
                        ],
                        type=DataSetFieldType(
                            type=Type.TYPE_STRUCT,
                            logical_type=field_type.to_logical_type(),
                            is_nullable=False,
                        ),
                        owner=None,
                        parent_field_oddrn=parent_oddrn,
                    )
                )
                for field_name, _type in field_type.fields.items():
                    _build_ds_field_from_type(field_name, _type, oddrn)
            elif isinstance(field_type, ArrayType):
                generated_dataset_fields.append(
                    DataSetField(
                        oddrn=oddrn,
                        name=field_name,
                        metadata=[
                            extract_metadata(
                                data_source, field, DefinitionType.DATASET_FIELD
                            )
                        ],
                        type=DataSetFieldType(
                            type=Type.TYPE_LIST,
                            logical_type=field_type.to_logical_type(),
                            is_nullable=False,
                        ),
                        owner=None,
                        parent_field_oddrn=parent_oddrn,
                    )
                )
                _build_ds_field_from_type("Element", field_type.element_type, oddrn)
            elif isinstance(field_type, MapType):
                generated_dataset_fields.append(
                    DataSetField(
                        oddrn=oddrn,
                        name=field_name,
                        metadata=[
                            extract_metadata(
                                data_source, field, DefinitionType.DATASET_FIELD
                            )
                        ],
                        type=DataSetFieldType(
                            type=Type.TYPE_MAP,
                            logical_type=field_type.to_logical_type(),
                            is_nullable=False,
                        ),
                        owner=None,
                        parent_field_oddrn=parent_oddrn,
                    )
                )
                _build_ds_field_from_type("Key", field_type.key_type, oddrn)
                _build_ds_field_from_type("Value", field_type.value_type, oddrn)
            elif isinstance(field_type, UnionType):
                generated_dataset_fields.append(
                    DataSetField(
                        oddrn=oddrn,
                        name=field_name,
                        metadata=[
                            extract_metadata(
                                data_source, field, DefinitionType.DATASET_FIELD
                            )
                        ],
                        type=DataSetFieldType(
                            type=Type.TYPE_UNION,
                            logical_type=field_type.to_logical_type(),
                            is_nullable=False,
                        ),
                        owner=None,
                        parent_field_oddrn=parent_oddrn,
                    )
                )

            else:
                odd_type = self.get_odd_type(field_type)
                logical_type = field_type.to_logical_type()
                logger.debug(
                    f"Column {field_name} has ODD type {odd_type} and logical type {logical_type}"
                )
                generated_dataset_fields.append(
                    DataSetField(
                        oddrn=oddrn,
                        name=field_name,
                        metadata=[
                            extract_metadata(
                                data_source, field, DefinitionType.DATASET_FIELD
                            )
                        ],
                        type=DataSetFieldType(
                            type=odd_type,
                            logical_type=logical_type,
                            is_nullable=False,
                        ),
                        owner=None,
                        parent_field_oddrn=parent_oddrn,
                    )
                )

        _build_ds_field_from_type(field.name, field_type)
        return generated_dataset_fields

    def get_odd_type(self, basic_type: BasicType) -> Type:
        return self.odd_types_map.get(basic_type.type_name, Type.TYPE_UNKNOWN)
