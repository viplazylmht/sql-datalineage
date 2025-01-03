from datalineage.node import Node, NodeType
import json


class SubqueryNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.SUBQUERY

    def __str__(self) -> str:
        return "SubqueryNode<{}>".format(json.dumps(self.to_json_dict()))
