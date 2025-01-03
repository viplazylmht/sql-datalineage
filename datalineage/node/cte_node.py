from datalineage.node import Node, NodeType
import json


class CTENode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.CTE

    def __str__(self) -> str:
        return "CTENode<{}>".format(json.dumps(self.to_json_dict()))
