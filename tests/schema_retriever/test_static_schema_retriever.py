import unittest
from sqlglot import exp

from .test_schema_retriever import TestSchemaRetrieverBase
from datalineage.schema_retriever.static_schema_retriever import StaticSchemaRetriever


class TestStaticSchemaRetriever(TestSchemaRetrieverBase):
    def setUp(self):
        self._dialect = "bigquery"
        self._schema_retriever = StaticSchemaRetriever(
            schema={
                "messages": {
                    "id": "int64",
                    "message": "string",
                    "send_on": "timestamp",
                },
                "profiles": {
                    "id": "string",
                    "name": "string",
                    "phone": "bigint",
                    "email": "string",
                },
            },
            dialect=self._dialect,
        )

        return super().setUp()

    def test_retrieve_schema(self):
        message_table = exp.to_table("messages")
        profile_table = "profiles"
        unknown_table = "unknown"

        self._schema_retriever.retrieve_schema(tables=[message_table, profile_table, unknown_table])
        schema = self._schema_retriever.schema

        self.validate_column_names(
            schema=schema,
            table=message_table,
            dialect=self._dialect,
            column_names={"id", "message", "send_on"},
        )
        self.validate_column_names(
            schema=schema,
            table=profile_table,
            dialect=self._dialect,
            column_names={"id", "name", "phone", "email"},
        )
        self.validate_column_names(
            schema=schema, table=unknown_table, dialect=self._dialect, column_names=set([])
        )

        self.validate_column_type(
            schema=schema,
            table=message_table,
            dialect=self._dialect,
            column="id",
            column_type=exp.DataType.build(dtype="int64", dialect=self._dialect),
        )

        self.validate_column_type(
            schema=schema,
            table=message_table,
            dialect=self._dialect,
            column="send_on",
            column_type=exp.DataType.build(dtype="timestamp", dialect=self._dialect),
        )

        self.validate_column_type(
            schema=schema,
            table=profile_table,
            dialect=self._dialect,
            column="email",
            column_type=exp.DataType.build(dtype="string", dialect=self._dialect),
        )

        self.validate_column_type(
            schema=schema,
            table=unknown_table,
            dialect=self._dialect,
            column="id",
            column_type=exp.DataType.build(dtype=exp.DataType.Type.UNKNOWN),
        )


if __name__ == "__main__":
    unittest.main()
