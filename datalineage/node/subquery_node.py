from datalineage.node import Node, NodeType
import json

from typing import TypeVar, TYPE_CHECKING

T = TypeVar("T")
if TYPE_CHECKING:
    from datalineage.node.node_visitor import NodeVisitor


class SubqueryNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.SUBQUERY

    def __str__(self) -> str:
        return "SubqueryNode<{}>".format(json.dumps(self.to_json_dict()))

    def accept(self, visitor: "NodeVisitor[T]") -> T:
        return visitor.visit_subquery(self)
