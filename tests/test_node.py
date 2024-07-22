import unittest
from sqlglot import exp, parse_one

from datalineage.node import Node, NodeType


class TestNode(unittest.TestCase):
    def validate_node_equal(self, first: Node, second: Node, target: bool):
        with self.subTest(
            "Test node equal: {} == {} => {}".format(first.name, second.name, target)
        ):
            self.assertEqual(first == second, target)

    def test_node(self):
        first_node = Node(
            name="first_column",
            expression=exp.to_column("table_1.column"),
            generated_expression=parse_one("select table_1.column from table table_1"),
            source_expression=parse_one("select * from data"),
            node_type=NodeType.COLUMN,
        )

        second_node = Node(
            name="first_column",
            expression=exp.to_column("table_1.column"),
            generated_expression=parse_one("select table_1.column from table table_1"),
            source_expression=parse_one("select * from data"),
            node_type=NodeType.COLUMN,
        )

        third_node = Node(
            name="second_column",
            expression=exp.to_column("table_1.column2"),
            generated_expression=parse_one("select table_1.column2 from table table_1"),
            source_expression=parse_one("select * from data"),
            node_type=NodeType.COLUMN,
        )

        self.validate_node_equal(first_node, second_node, True)
        self.validate_node_equal(first_node, third_node, False)
        self.validate_node_equal(second_node, third_node, False)


if __name__ == "__main__":
    unittest.main()
