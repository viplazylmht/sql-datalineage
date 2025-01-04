from datalineage.node import (
    NodeVisitor,
    Node,
    ColumnNode,
    TableNode,
    SelectNode,
    SubqueryNode,
    UnionNode,
    UnionAllNode,
    CTENode,
    UnknownNode,
)

from sqlglot.dialects.dialect import DialectType


class PrettyNameVisitor(NodeVisitor[str]):
    def __init__(self, dialect: DialectType = None):
        self.dialect = dialect

    def _get_node_name_str(self, node: Node) -> str:
        return node.name if isinstance(node.name, str) else node.name.sql(self.dialect)

    def visit_column(self, node: ColumnNode) -> str:
        return "Column: " + self._get_node_name_str(node)

    def visit_table(self, node: TableNode) -> str:
        return "Table: " + self._get_node_name_str(node)

    def visit_select(self, node: SelectNode) -> str:
        return "Select Statement: " + self._get_node_name_str(node)

    def visit_subquery(self, node: SubqueryNode) -> str:
        return "Subquery: " + self._get_node_name_str(node)

    def visit_union(self, node: UnionNode) -> str:
        return "Union: " + self._get_node_name_str(node)

    def visit_union_all(self, node: UnionAllNode) -> str:
        return "Union All: " + self._get_node_name_str(node)

    def visit_cte(self, node: CTENode) -> str:
        return "CTE: " + self._get_node_name_str(node)

    def visit_unknown(self, node: UnknownNode) -> str:
        return "Unknown Node: " + self._get_node_name_str(node)
