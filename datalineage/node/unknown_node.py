from datalineage.node import Node, NodeType
import json


class UnknownNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.UNKNOWN

    def __str__(self) -> str:
        return "UnknownNode<{}>".format(json.dumps(self.to_json_dict()))
