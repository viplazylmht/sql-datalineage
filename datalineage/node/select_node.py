from datalineage.node import Node, NodeType
import json

from typing import TypeVar, TYPE_CHECKING

T = TypeVar("T")
if TYPE_CHECKING:
    from datalineage.node.node_visitor import NodeVisitor


class SelectNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.SELECT

    def __str__(self) -> str:
        return "SelectNode<{}>".format(json.dumps(self.to_json_dict()))

    def accept(self, visitor: "NodeVisitor[T]") -> T:
        return visitor.visit_select(self)
