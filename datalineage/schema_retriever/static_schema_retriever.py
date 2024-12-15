from sqlglot.schema import Schema, ensure_schema
from sqlglot import exp
from typing import Optional, Union, Dict

from datalineage.schema_retriever.schema_retriever import SchemaRetriever


class StaticSchemaRetriever(SchemaRetriever):
    def __init__(self, schema: Optional[Union[Schema, Dict]] = None, dialect: Optional[str] = None):
        self._schema = ensure_schema(schema=schema, dialect=dialect)

    def retrieve_table_schema(self, table: exp.Table) -> Optional[Dict]:
        column_defs = {
            column: self._schema.get_column_type(table=table, column=column)
            for column in self._schema.column_names(table=table)
        }

        if column_defs:
            return column_defs

        return None
