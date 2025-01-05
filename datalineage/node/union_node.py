from datalineage.node import Node, NodeType
import json

from typing import TypeVar, TYPE_CHECKING

T = TypeVar("T")
if TYPE_CHECKING:
    from datalineage.node.node_visitor import NodeVisitor


class UnionNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.UNION

    def __str__(self) -> str:
        return "UnionNode<{}>".format(json.dumps(self.to_json_dict()))

    def accept(self, visitor: "NodeVisitor[T]") -> T:
        return visitor.visit_union(self)


class UnionAllNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.UNION_ALL

    def __str__(self) -> str:
        return "UnionAllNode<{}>".format(json.dumps(self.to_json_dict()))

    def accept(self, visitor: "NodeVisitor[T]") -> T:
        return visitor.visit_union_all(self)
