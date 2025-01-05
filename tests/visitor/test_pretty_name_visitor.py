from datalineage.visitor.pretty_name_visitor import PrettyNameVisitor
from datalineage.node import (
    ColumnNode,
    TableNode,
)

import unittest
from sqlglot import exp


class TestPrettyNameVisitor(unittest.TestCase):
    def test_pretty_name_visitor(self):
        pretty_name_visitor = PrettyNameVisitor()

        col_name = "age"
        self.assertEqual(
            ColumnNode(name=col_name, expression=exp.to_column(col_name)).accept(
                pretty_name_visitor
            ),
            f"Column: {col_name}",
        )
        self.assertEqual(
            ColumnNode(name=exp.to_column(col_name), expression=exp.to_column(col_name)).accept(
                pretty_name_visitor
            ),
            f"Column: {col_name}",
        )

        table_exp = exp.Table(
            this=exp.Identifier(this="users", quoted=True),
            db=exp.Identifier(this="DATASET", quoted=True),
            catalog=exp.Identifier(this="project", quoted=True),
            alias=exp.TableAlias(this=exp.Identifier(this="u", quoted=False)),
        )
        table_node = TableNode(name=table_exp, expression=table_exp)

        self.assertEqual(
            table_node.accept(PrettyNameVisitor(dialect="bigquery")),
            "Table: `project`.`DATASET`.`users` AS u",
        )

        self.assertEqual(
            table_node.accept(PrettyNameVisitor(dialect="trino")),
            'Table: "project"."DATASET"."users" AS u',
        )


if __name__ == "__main__":
    unittest.main()
