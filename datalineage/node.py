from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Union
from sqlglot import exp


class NodeType(str, Enum):
    TABLE = "Table"
    CTE = "CTE"
    SUBQUERY = "Subquery"
    SELECT = "Select"
    CREATE = "Create"
    MERGE = "Merge"
    INSERT = "INSERT"
    UPDATE = "Update"
    COLUMN = "Column"
    UNKNOWN = "Unknown"


@dataclass
class Node:
    name: Union[str, exp.Expression]
    expression: exp.Expression
    generated_expression: Optional[exp.Expression]
    source_expression: Optional[exp.Expression]
    _parent: Optional["Node"] = None
    node_type: Optional[NodeType] = None
    children: List["Node"] = field(default_factory=list)
    downstreams: List["Node"] = field(default_factory=list)

    def add_downstream(self, downstream: "Node") -> "Node":
        if downstream not in self.downstreams:
            self.downstreams.append(downstream)
        return self

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent: Optional["Node"]):
        self._parent = parent

    @parent.deleter
    def parent(self):
        self._parent = None

    def add_child(self, child: "Node") -> "Node":
        if child not in self.children:
            if child.parent:
                raise ValueError("the child is already occupied by another parent.")

            child.parent = self
            self.children.append(child)
        return self

    def get_child_by_name(self, child_name: str) -> Optional["Node"]:
        """Get a child of this node, return None if not found."""
        resolved_child = None

        for child in self.children:
            if child_name == child.name:
                resolved_child = child
                break

        return resolved_child

    def walk(self):
        """Pre-Order DFS"""
        yield self

        for d in self.downstreams:
            yield from d.walk()

    def reversed_walk(self):
        """Post-Order DFS"""
        for d in self.downstreams:
            yield from d.reversed_walk()

        yield self

    def to_json_dict(self) -> dict:
        result = dict(
            id=id(self),
            name=str(self.name),
            expression=self.expression.sql(),
            generated_expression=self.generated_expression.sql()
            if self.generated_expression
            else None,
            source_expression=self.source_expression.sql() if self.source_expression else None,
            node_type=self.node_type if self.node_type else None,
            children=[child.to_json_dict() for child in self.children],
            downstreams=[downstream.to_json_dict() for downstream in self.downstreams],
        )
        return result

    def lookup(self, expression: exp.Expression) -> Optional["Node"]:
        """traversal from this root through downstreams to get a node containing the expression (if exist)"""

        for node in self.walk():
            if node.expression == expression:
                return node

        return None

    def __str__(self):
        return f"Node<{self.name}>"
