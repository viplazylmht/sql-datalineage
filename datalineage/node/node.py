from copy import deepcopy
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict, TypeVar, TYPE_CHECKING
from sqlglot import exp
import json
from hashlib import sha256

T = TypeVar("T")
if TYPE_CHECKING:
    from datalineage.node.node_visitor import NodeVisitor


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
    UNION = "Union"
    UNION_ALL = "Union All"
    UNKNOWN = "Unknown"


@dataclass
class Node:
    name: Union[str, exp.Expression]
    expression: exp.Expression
    generated_expression: Optional[exp.Expression] = None
    source_expression: Optional[exp.Expression] = None
    _parent: Optional["Node"] = None
    children: List["Node"] = field(default_factory=list)
    upstreams: List["Node"] = field(default_factory=list)
    downstreams: List["Node"] = field(default_factory=list)

    @property
    def node_type(self) -> NodeType:
        raise NotImplementedError

    @property
    def node_id(self) -> int:
        return int.from_bytes(
            sha256(json.dumps(self._build_node_dict()).encode()).digest()[:8],
            byteorder="big",
            signed=False,
        )

    def add_downstream(self, downstream: "Node") -> "Node":
        if not self.has_downstream(downstream):
            self.downstreams.append(downstream)

        if not downstream.has_upstream(self):
            downstream.add_upstream(self)

        return self

    def has_downstream(self, node: "Node") -> bool:
        node_id = node.node_id
        return any(map(lambda n: n.node_id == node_id, self.downstreams))

    def add_upstream(self, upstream: "Node") -> "Node":
        if not self.has_upstream(upstream):
            self.upstreams.append(upstream)

        if not upstream.has_downstream(self):
            upstream.add_downstream(self)

        return self

    def has_upstream(self, node: "Node") -> bool:
        node_id = node.node_id
        return any(map(lambda n: n.node_id == node_id, self.upstreams))

    def has_child(self, child: "Node") -> bool:
        child_id = child.node_id
        return any(map(lambda n: n.node_id == child_id, self.children))

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
        if not self.has_child(child):
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

    def walk(self, downstream=True, upstream=True):
        """Pre-Order DFS"""
        yield self

        if downstream:
            yield from self.downstream_walk(reverse=False)

        if upstream:
            yield from self.upstream_walk(reverse=False)

    def downstream_walk(self, reverse=False):
        """Pre-Order DFS"""
        for d in self.downstreams:
            if not reverse:
                yield d
                yield from d.downstream_walk(reverse=reverse)
            else:
                yield from d.downstream_walk(reverse=reverse)
                yield d

    def upstream_walk(self, reverse=False):
        """Pre-Order DFS"""
        for u in self.upstreams:
            if not reverse:
                yield u
                yield from u.upstream_walk(reverse=reverse)
            else:
                yield from u.upstream_walk(reverse=reverse)
                yield u

    def reversed_walk(self, downstream=True, upstream=True):
        """Post-Order DFS"""

        if downstream:
            yield from self.downstream_walk(reverse=True)

        if upstream:
            yield from self.upstream_walk(reverse=True)

        yield self

    def _build_node_dict(self) -> dict:
        return dict(
            name=str(self.name),
            expression=self.expression.sql(),
            generated_expression=self.generated_expression.sql()
            if self.generated_expression
            else None,
            source_expression=self.source_expression.sql() if self.source_expression else None,
            node_type=self.node_type.value
            if isinstance(self.node_type, NodeType)
            else self.node_type
            if self.node_type
            else None,
            parent_id=self.parent.node_id if self.parent else None,
        )

    def to_json_dict(self) -> dict:
        nodes: Dict[int, Dict] = {}
        edges: Dict[int, List[int]] = {}
        children: Dict[int, List[int]] = {}

        for node in self.walk():
            node_id = node.node_id

            if node_id not in nodes:
                nodes[node_id] = node._build_node_dict()

                for child in node.children:
                    child_id = child.node_id
                    if child_id not in nodes:
                        nodes[child_id] = child._build_node_dict()

                    if node_id not in children:
                        children[node_id] = [child_id]
                    elif child_id not in children[node_id]:
                        children[node_id].append(child_id)

                for downstream in node.downstreams:
                    downstream_id = downstream.node_id
                    if node_id not in edges:
                        edges[node_id] = [downstream_id]
                    elif downstream_id not in edges[node_id]:
                        edges[node_id].append(downstream_id)

                for upstream in node.upstreams:
                    upstream_id = upstream.node_id
                    if upstream_id not in edges:
                        edges[upstream_id] = [node_id]
                    elif node_id not in edges[upstream_id]:
                        edges[upstream_id].append(node_id)

        return dict(nodes=nodes, edges=edges, children=children)

    def __str__(self) -> str:
        return "Node<{}>".format(json.dumps(self.to_json_dict()))

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__hash__() == other.__hash__()
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        else:
            return NotImplemented

    def copy(self):
        """
        Returns a deep copy of the node.
        """
        return deepcopy(self)

    def lookup(self, expression: exp.Expression) -> Optional["Node"]:
        """traversal from this root through downstreams to get a node containing the expression (if exist)"""

        for node in self.walk():
            if node.expression == expression:
                return node

        return None

    def accept(self, visitor: "NodeVisitor[T]") -> T:
        raise NotImplementedError
