from datalineage.node import Node, NodeType
import json


class TableNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.TABLE

    def __str__(self) -> str:
        return "TableNode<{}>".format(json.dumps(self.to_json_dict()))
