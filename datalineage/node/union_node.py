from datalineage.node import Node, NodeType
import json


class UnionNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.UNION

    def __str__(self) -> str:
        return "UnionNode<{}>".format(json.dumps(self.to_json_dict()))


class UnionAllNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.UNION_ALL

    def __str__(self) -> str:
        return "UnionAllNode<{}>".format(json.dumps(self.to_json_dict()))
