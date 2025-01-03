from datalineage.node import Node, NodeType
import json


class ColumnNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.COLUMN

    def __str__(self) -> str:
        return "ColumnNode<{}>".format(json.dumps(self.to_json_dict()))
