import unittest
from sqlglot import exp
from sqlglot.schema import Schema
from typing import Union, Set


class TestSchemaRetriever(unittest.TestCase):
    """Base class to allow testing on subclass."""

    def validate_column_names(
        self, schema: Schema, table: Union[exp.Table, str], dialect: str, column_names: Set[str]
    ):
        with self.subTest(
            "test set of column names of table {} = {}".format(str(table), column_names)
        ):
            self.assertEqual(set(schema.column_names(table=table, dialect=dialect)), column_names)

    def validate_column_type(
        self,
        schema: Schema,
        table: Union[exp.Table, str],
        dialect: str,
        column: str,
        column_type: exp.DataType,
    ):
        with self.subTest(
            "test data type of column {} in table {} = {}".format(column, str(table), column_type)
        ):
            self.assertEqual(
                schema.get_column_type(table=table, column=column, dialect=dialect),
                column_type,
            )
