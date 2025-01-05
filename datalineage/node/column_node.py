from datalineage.node import Node, NodeType
import json

from typing import TypeVar, TYPE_CHECKING


T = TypeVar("T")
if TYPE_CHECKING:
    from datalineage.node.node_visitor import NodeVisitor


class ColumnNode(Node):
    @property
    def node_type(self) -> NodeType:
        return NodeType.COLUMN

    def __str__(self) -> str:
        return "ColumnNode<{}>".format(json.dumps(self.to_json_dict()))

    def accept(self, visitor: "NodeVisitor[T]") -> T:
        return visitor.visit_column(self)
