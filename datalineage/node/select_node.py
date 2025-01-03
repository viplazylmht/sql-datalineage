from datalineage.node import Node, NodeType
import json


class SelectNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.SELECT

    def __str__(self) -> str:
        return "SelectNode<{}>".format(json.dumps(self.to_json_dict()))
