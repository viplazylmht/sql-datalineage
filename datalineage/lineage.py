from sqlglot.optimizer.scope import Scope, ScopeType
from sqlglot.schema import Schema, ensure_schema
from sqlglot import exp, parse_one
from sqlglot.optimizer.scope import build_scope, find_all_in_scope
from sqlglot.optimizer.qualify import qualify

from typing import Dict, Optional, Any, Union, List

from datalineage.node import Node, NodeType
from datalineage.logger import setup_logger

logger = setup_logger(__name__)


def get_destination_node(ast: exp.Expression) -> Optional[Node]:
    if isinstance(ast, exp.Insert) or isinstance(ast, exp.Create):
        dest_exp = ast.this

        table_exp: exp.Table
        columns: List[exp.Identifier] = []

        if isinstance(dest_exp, exp.Table):
            table_exp = dest_exp
        elif isinstance(dest_exp, exp.Schema):
            table_exp = dest_exp.this
            columns = dest_exp.expressions
        else:
            logger.info(
                "Only support insert in to table or schema, currently {}".format(type(dest_exp))
            )

        dest_node = Node(
            name=table_exp.sql(),
            expression=table_exp,
            generated_expression=None,  # TODO: generated_expression of a Table is select * from this table
            source_expression=None,  # TODO: source_expression should be "FROM {Table}"
            node_type=NodeType.TABLE,
        )

        for column in columns:
            child_node = Node(
                name=column.this,
                expression=column,
                generated_expression=column,
                source_expression=dest_exp,
                node_type=NodeType.COLUMN,
            )
            dest_node.add_child(child_node)

        return dest_node

    return None


def create_column_for_table(table_node: Node, column_name: str):
    dest_column_select_expression = exp.select(column_name).from_(table_node.expression)
    dest_child = Node(
        name=column_name,
        expression=exp.to_identifier(column_name, quoted=False),
        generated_expression=dest_column_select_expression,
        source_expression=dest_column_select_expression,
        node_type=NodeType.COLUMN,
    )
    table_node.add_child(dest_child)


def link_source_to_dest(dest_table: Node, schema: Schema):
    if len(dest_table.downstreams) != 1:
        logger.info(
            "Can not link source to dest. Dest table should contains only one SELECT downstream, currently; {}".format(
                len(dest_table.downstreams)
            )
        )
        return
    elif dest_table.downstreams[0].node_type != NodeType.SELECT:
        logger.info(
            "Can not link source to dest. Dest table downstream should be a select statement."
        )
        return

    select_downstream = dest_table.downstreams[0]
    if len(dest_table.children) > 0 and len(dest_table.children) != len(select_downstream.children):
        raise Exception("Can not build lineage for this statement. Missmatch number of columns.")

    if isinstance(dest_table.expression, exp.Table):
        dest_schema_columns = schema.column_names(dest_table.expression)
        if len(dest_table.children) == 0:
            dest_columns = dest_schema_columns or list(
                map(
                    lambda x: x.name.sql() if isinstance(x.name, exp.Expression) else x.name,
                    select_downstream.children,
                )
            )

            for column_name in dest_columns:
                create_column_for_table(table_node=dest_table, column_name=column_name)
        else:
            # validate schema
            if dest_schema_columns:
                for child in dest_table.children:
                    if child.name not in dest_schema_columns:
                        raise Exception(
                            "Column {} not found in the schema of table {}. Available columns: {}".format(
                                child.name, dest_table.expression.sql(), dest_schema_columns
                            )
                        )

            for schema_column in dest_schema_columns:
                if not dest_table.get_child_by_name(schema_column):
                    create_column_for_table(table_node=dest_table, column_name=schema_column)

        for dest_child, select_child in zip(dest_table.children, select_downstream.children):
            dest_child.add_downstream(select_child)


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
        this_relation: Optional[exp.Expression] = None
        from_expression: exp.From = scope.expression.args.get("from")  # type: ignore
        if from_expression:
            this_relation = from_expression.this

        subquery_scopes = {
            id(subquery_scope.expression): subquery_scope
            for subquery_scope in scope.subquery_scopes
        }

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
            node_name = this_relation.alias_or_name  # type: ignore
        elif scope.scope_type == ScopeType.CTE:
            node_type = NodeType.CTE

        if not this_relation:
            this_node = Node(
                name=node_name,
                expression=exp.Literal(this="empty node", is_string=True),
                generated_expression=scope.expression,
                source_expression=scope.expression,
                node_type=node_type,
            )
        else:
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
                    continue

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

            for subquery in find_all_in_scope(select, exp.UNWRAPPED_QUERIES):
                subquery_scope = subquery_scopes.get(id(subquery))

                if subquery_scope:
                    subquery_node = create_node(
                        root_node=root_node,
                        upstream=this_node,
                        node_name="Scalar subquery",
                        scope=subquery_scope,
                        schema=schema,
                    )

                    if subquery_node:
                        child_node.add_downstream(subquery_node)

                else:
                    logger.error(
                        "The suquery {} in column {} was not found in the parent scope".format(
                            str(subquery), select.alias_or_name
                        )
                    )

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

    root_table = exp.to_identifier("ANCHOR")
    root_node = Node(
        name="myroot",
        expression=root_table,
        generated_expression=ast,
        source_expression=ast,
        node_type=NodeType.SELECT,
    )

    dest_table: Optional[Node] = get_destination_node(ast)
    if dest_table:
        root_node.add_downstream(dest_table)

    if scp:
        create_node(root_node, dest_table or root_node, "idk", scp, schema)

        # link output to dest table
        if dest_table:
            link_source_to_dest(dest_table=dest_table, schema=schema)

    return root_node
