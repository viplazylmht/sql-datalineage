from sqlglot import Schema, exp
from typing import Optional, Dict, Union
from datalineage.schema_retriever.schema_retriever import SchemaRetriever
from sqlalchemy import inspect, Engine


class SQLAlchemySchemaRetriever(SchemaRetriever):
    def __init__(
        self,
        engine: Engine,
        schema: Optional[Union[Schema, Dict]] = None,
        dialect: Optional[str] = None,
    ):
        super().__init__(schema=schema, dialect=dialect)
        self._engine = engine

    def retrieve_table_schema(self, table: exp.Table) -> Optional[Dict]:
        inspector = inspect(self._engine)

        columns = inspector.get_columns(table_name=table.text("this"), schema=table.db or None)

        if isinstance(columns, list):
            return {column.get("name"): str(column.get("type")) for column in columns}

        return None
