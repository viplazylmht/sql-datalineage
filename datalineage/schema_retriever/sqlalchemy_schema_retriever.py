from sqlglot import exp
from typing import Optional, Dict
from datalineage.schema_retriever.schema_retriever import SchemaRetriever
from sqlalchemy import inspect, create_engine, Engine


class SQLAlchemySchemaRetriever(SchemaRetriever):
    def __init__(self, *engine_args, engine: Optional[Engine] = None, **engine_kwargs):
        self._engine = engine if engine else create_engine(*engine_args, **engine_kwargs)
        self._inspector = inspect(self._engine)

    def retrieve_table_schema(self, table: exp.Table) -> Optional[Dict]:
        columns = self._inspector.get_columns(
            table_name=table.text("this"), schema=table.db or None
        )

        if isinstance(columns, list):
            return {column.get("name"): str(column.get("type")) for column in columns}

        return None
