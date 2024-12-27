from datalineage.serializer.serializer import Serializer
from datalineage.lineage import lineage, Node

import unittest
from typing import TypeVar
from unittest import TestCase

T = TypeVar("T")


class TestSerializer(TestCase):
    def validate_serializer(self, serializer: Serializer, input: T, expected_output: T):
        with self.subTest("test serializer -> {}".format(input)):
            serialized_data = serializer.serialize(input)
            deserialized_data = serializer.deserialize(serialized_data)

            self.assertIsInstance(serialized_data, bytes)
            self.assertIsInstance(deserialized_data, type(input))

            self.assertEqual(expected_output, deserialized_data)

    def test_serializer(self):
        dict_serializer: Serializer[dict] = Serializer()
        dict_data = {
            "int": 1,
            "float": 1.0,
            "str": "string",
            "list": [1, 2, 3],
            "dict": {"key": "value"},
        }
        self.validate_serializer(
            serializer=dict_serializer, input=dict_data, expected_output=dict_data
        )

        node_serializer: Serializer[Node] = Serializer()
        node_data = lineage(sql="SELECT * FROM (SELECT col_1, col2 FROM table_a a)")
        self.validate_serializer(
            serializer=node_serializer, input=node_data, expected_output=node_data
        )


if __name__ == "__main__":
    unittest.main()
