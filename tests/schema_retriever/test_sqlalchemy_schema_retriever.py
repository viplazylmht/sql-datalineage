import unittest
import os
import gc
import pathlib
from sqlglot import exp
from sqlalchemy import create_engine, text

from .test_schema_retriever import TestSchemaRetriever
from datalineage.schema_retriever.sqlalchemy_schema_retriever import SQLAlchemySchemaRetriever


class TestSqlalchemySchemaRetriever(TestSchemaRetriever):
    PATH = pathlib.Path(__file__).parent.resolve()

    def setUp(self):
        self._sqlite_db_file_path = str(self.PATH / "database.db")
        self._sqlite_engine = create_engine("sqlite:///{}".format(self._sqlite_db_file_path))
        with self._sqlite_engine.connect() as conn:
            conn.execute(
                text("create table if not exists messages(id int, message text, send_on timestamp)")
            )
            conn.execute(
                text(
                    "create table if not exists profiles(id int, name text, phone int, email text)"
                )
            )

        self._sqlite_create_engine_params = ("sqlite:///{}".format(self._sqlite_db_file_path),)

        return super().setUp()

    def tearDown(self):
        del self._sqlite_engine
        # force collect gc to be able to remove the db file on Windows
        gc.collect()
        if os.path.isfile(self._sqlite_db_file_path):
            os.remove(self._sqlite_db_file_path)

        return super().tearDown()

    def validate_sqlite_retriever(self, sqlite_retriever: SQLAlchemySchemaRetriever):
        base_schema = None
        dialect = "sqlite"
        message_table = exp.to_table("messages")
        profile_table = "profiles"
        unknown_table = "unknown"

        schema = sqlite_retriever.retrieve_schema(
            base_schema=base_schema,
            tables=[message_table, profile_table, unknown_table],
            dialect=dialect,
        )

        self.validate_column_names(
            schema=schema,
            table=message_table,
            dialect=dialect,
            column_names={"id", "message", "send_on"},
        )
        self.validate_column_names(
            schema=schema,
            table=profile_table,
            dialect=dialect,
            column_names={"id", "name", "phone", "email"},
        )
        self.validate_column_names(
            schema=schema, table=unknown_table, dialect=dialect, column_names=set([])
        )

        self.validate_column_type(
            schema=schema,
            table=message_table,
            dialect=dialect,
            column="id",
            column_type=exp.DataType.build(dtype="int", dialect=dialect),
        )

        self.validate_column_type(
            schema=schema,
            table=message_table,
            dialect=dialect,
            column="send_on",
            column_type=exp.DataType.build(dtype="timestamp", dialect=dialect),
        )

        self.validate_column_type(
            schema=schema,
            table=profile_table,
            dialect=dialect,
            column="email",
            column_type=exp.DataType.build(dtype="text", dialect=dialect),
        )

        self.validate_column_type(
            schema=schema,
            table=unknown_table,
            dialect=dialect,
            column="id",
            column_type=exp.DataType.build(dtype=exp.DataType.Type.UNKNOWN),
        )

    def test_retrieve_schema(self):
        with self.subTest("test retrieve schema sqlite from engine"):
            sqlite_engine_schema_retriever = SQLAlchemySchemaRetriever(engine=self._sqlite_engine)
            self.validate_sqlite_retriever(sqlite_retriever=sqlite_engine_schema_retriever)

        with self.subTest("test retrieve schema sqlite from create engine params"):
            sqlite_engine_schema_retriever = SQLAlchemySchemaRetriever(
                *self._sqlite_create_engine_params
            )
            self.validate_sqlite_retriever(sqlite_retriever=sqlite_engine_schema_retriever)


if __name__ == "__main__":
    unittest.main()
