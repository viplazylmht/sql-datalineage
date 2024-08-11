from sqlglot.optimizer.scope import Scope, ScopeType
from sqlglot.schema import Schema, ensure_schema
from sqlglot import exp, parse_one
from sqlglot.optimizer.scope import build_scope
from sqlglot.optimizer.qualify import qualify

from typing import Dict, Optional, Any, Union

from datalineage.node import Node, NodeType
from datalineage.logger import setup_logger

logger = setup_logger(__name__)


def create_node(
    root_node: Node,
    upstream: Node,
    node_name: str,
    scope: Union[Scope, exp.Table, None],
    schema: Schema,
) -> Node:
    if isinstance(scope, Scope):
        if isinstance(scope.expression, exp.Union):
            union_node = (
                upstream
                if upstream.node_type == NodeType.UNION
                else Node(
                    name="Union",
                    expression=scope.expression,
                    generated_expression=scope.expression,
                    source_expression=scope.expression,
                    node_type=NodeType.UNION,
                )
            )
            if id(upstream) != id(union_node):
                upstream.add_downstream(union_node)

            left_expression = scope.expression.left
            left_expression.set("with", scope.expression.args.get("with"))

            left_node = create_node(
                root_node=root_node,
                upstream=union_node,
                node_name="Union Slot",
                scope=build_scope(left_expression),
                schema=schema,
            )
            if id(union_node) != id(left_node):
                for c in left_node.children:
                    expression = exp.to_column(c.name)  # type: ignore
                    child = Node(
                        name=c.name,
                        expression=expression,
                        generated_expression=expression,
                        source_expression=scope.expression,
                        node_type=NodeType.COLUMN,
                    )
                    child.add_downstream(c)
                    union_node.add_child(child=child)

            right_expression = scope.expression.right
            right_expression.set("with", scope.expression.args.get("with"))

            right_node = create_node(
                root_node=root_node,
                upstream=union_node,
                node_name="Union Slot",
                scope=build_scope(right_expression),
                schema=schema,
            )
            for i, c in enumerate(right_node.children, 0):
                union_node.children[i].add_downstream(c)

            return union_node

        # create upstream
        elif not isinstance(scope.expression, exp.Select):
            raise ValueError(
                "Expected a select statement, actually got {}.".format(scope.expression)
            )

        this_relation = scope.expression.args.get("from").this  # type: ignore

        node_type = NodeType.SELECT
        if upstream.node_type == NodeType.UNION:
            node_name = node_name + f"#{len(upstream.downstreams)}"
        elif scope.scope_type == ScopeType.ROOT:
            this_relation = exp.Table(
                this=exp.to_identifier("ROOT_TABLE"),
                catalog=exp.to_identifier("catalog"),
                db=exp.to_identifier("myschema"),
            )
            node_name = "_output_"
        elif scope.scope_type == ScopeType.DERIVED_TABLE:
            node_type = NodeType.SUBQUERY
            this_relation = scope.expression.parent
            node_name = this_relation.alias_or_name
        elif scope.scope_type == ScopeType.CTE:
            node_type = NodeType.CTE

        this_node = Node(
            name=node_name,
            expression=this_relation,
            generated_expression=scope.expression,
            source_expression=scope.expression,
            node_type=node_type,
        )
        upstream.add_downstream(this_node)

        nodes: Dict[str, Node] = {}
        for table_name, child_source in scope.selected_sources.items():
            child_table, child_scope = child_source
            name = child_table
            new_node = create_node(root_node, this_node, name, child_scope, schema)
            nodes[table_name] = new_node

        scope_selects = scope.expression.selects
        for select in scope_selects:
            if not isinstance(select, exp.Alias):
                raise ValueError("Please qualify the query to alias all columns")

            output_col_name = select.output_name
            output_col_expression = select.this

            child_node = Node(
                name=output_col_name,
                expression=output_col_expression,
                generated_expression=output_col_expression,
                source_expression=scope.expression,
                node_type=NodeType.COLUMN,
            )
            this_node.add_child(child_node)

            # link columns
            for c_dep in select.find_all(exp.Column):
                c_table = c_dep.table
                c_name = c_dep.output_name

                parent_node = nodes.get(c_table)
                if not parent_node:
                    raise ValueError(
                        f"Column {c_dep} does not belongs to any table in set {nodes.keys()}"
                    )

                parent_child = parent_node.get_child_by_name(c_name)

                # create new child column for the table node (infer the schema of the table node)
                if not parent_child:
                    parent_source = scope.selected_sources.get(c_table)
                    if isinstance(parent_source, tuple) and isinstance(parent_source[1], exp.Table):
                        parent_child = Node(
                            name=c_name,
                            expression=exp.Column(this=exp.to_identifier(c_name)),
                            generated_expression=parent_source[1].parent,
                            source_expression=parent_source[1].parent,
                            node_type=NodeType.COLUMN,
                        )
                        parent_node.add_child(parent_child)

                if parent_child:
                    child_node.add_downstream(parent_child)

        return this_node

    elif isinstance(scope, exp.Table):
        # this is tail node
        tail_node = Node(
            name=node_name,
            expression=scope,
            generated_expression=None,  # TODO: generated_expression of a Table is select * from this table
            source_expression=None,  # TODO: source_expression should be "FROM {Table}"
            node_type=NodeType.TABLE,
        )
        upstream.add_downstream(tail_node)

        column_names = schema.column_names(scope)
        for c_name in column_names:
            child_node = Node(
                name=c_name,
                expression=exp.Column(this=exp.to_identifier(c_name)),
                generated_expression=scope.parent,
                source_expression=scope.parent,
                node_type=NodeType.COLUMN,
            )
            tail_node.add_child(child_node)

        return tail_node
    else:
        logger.info(f"WARN: unexpected lineage with source: {scope}")
        tail_node = Node(
            name="<unknown>",
            expression=scope or exp.Literal(this="<unknown>"),
            generated_expression=None,  # TODO: generated_expression of a Table is select * from this table
            source_expression=None,  # TODO: source_expression should be "FROM {Table}"
            node_type=NodeType.UNKNOWN,
        )
        upstream.add_downstream(tail_node)

        return tail_node


def lineage(sql: str, dialect: Optional[Any] = None, schema: Optional[Any] = None):
    ast = parse_one(sql, read=dialect)

    # TODO: check DML and DDL here and remove the DML, DDL part
    schema = ensure_schema(schema, dialect=dialect)
    ast = qualify(
        ast, schema=schema, validate_qualify_columns=False, infer_schema=True, dialect=dialect
    )
    scp = build_scope(ast)

    if not scp:
        raise Exception(
            "Can not build lineage for this statement. Only accept select or DML or DDL queries."
        )

    root_table = exp.to_identifier("ANCHOR")
    root_node = Node(
        name="myroot",
        expression=root_table,
        generated_expression=ast,
        source_expression=ast,
        node_type=NodeType.SELECT,
    )

    create_node(root_node, root_node, "idk", scp, schema)

    return root_node
