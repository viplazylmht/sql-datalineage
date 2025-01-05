from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from datalineage.node import (
    ColumnNode,
    TableNode,
    CTENode,
    SubqueryNode,
    SelectNode,
    UnionNode,
    UnionAllNode,
    UnknownNode,
)

T = TypeVar("T")


class NodeVisitor(ABC, Generic[T]):
    @abstractmethod
    def visit_column(self, node: ColumnNode) -> T:
        raise NotImplementedError

    @abstractmethod
    def visit_table(self, node: TableNode) -> T:
        raise NotImplementedError

    @abstractmethod
    def visit_cte(self, node: CTENode) -> T:
        raise NotImplementedError

    @abstractmethod
    def visit_subquery(self, node: SubqueryNode) -> T:
        raise NotImplementedError

    @abstractmethod
    def visit_select(self, node: SelectNode) -> T:
        raise NotImplementedError

    @abstractmethod
    def visit_union(self, node: UnionNode) -> T:
        raise NotImplementedError

    @abstractmethod
    def visit_union_all(self, node: UnionAllNode) -> T:
        raise NotImplementedError

    @abstractmethod
    def visit_unknown(self, node: UnknownNode) -> T:
        raise NotImplementedError
