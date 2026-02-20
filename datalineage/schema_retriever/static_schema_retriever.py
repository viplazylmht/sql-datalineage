from sqlglot.schema import Schema
from sqlglot import exp
from typing import Optional, Union, Dict

from datalineage.schema_retriever.schema_retriever import SchemaRetriever


class StaticSchemaRetriever(SchemaRetriever):
    def __init__(self, schema: Optional[Union[Schema, Dict]] = None, dialect: Optional[str] = None):
        super().__init__(schema=schema, dialect=dialect)

    def retrieve_table_schema(self, table: exp.Table) -> Optional[Dict]:
        schema = self.schema
        column_defs = {
            column: schema.get_column_type(table=table, column=column)
            for column in schema.column_names(table=table)
        }

        if column_defs:
            return column_defs

        return None
