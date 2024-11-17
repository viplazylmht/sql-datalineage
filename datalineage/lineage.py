from sqlglot.optimizer.scope import Scope, ScopeType
from sqlglot.schema import Schema, ensure_schema
from sqlglot import exp, parse_one
from sqlglot.optimizer.scope import build_scope, find_all_in_scope
from sqlglot.optimizer.qualify import qualify

from typing import Dict, Optional, Any, Union, List

from datalineage.node import Node, NodeType
from datalineage.logger import setup_logger

logger = setup_logger(__name__)


def qualify_ast(ast: exp.Expression, schema: Schema, dialect: Optional[Any]) -> exp.Expression:
    ast = qualify(
        ast.copy(),
        schema=schema,
        validate_qualify_columns=False,
        infer_schema=True,
        dialect=dialect,
    )
    if isinstance(ast, exp.Merge):
        merge_using = ast.args.get("using")
        if isinstance(merge_using, exp.Subquery):
            qualify(
                merge_using,
                schema=schema,
                validate_qualify_columns=False,
                infer_schema=True,
                dialect=dialect,
            )

    return ast


def get_destination_node(ast: exp.Expression) -> Optional[Node]:
    table_exp: Optional[exp.Table] = None
    columns: List[exp.Identifier] = []
    if isinstance(ast, exp.Insert) or isinstance(ast, exp.Create):
        dest_exp = ast.this

        if isinstance(dest_exp, exp.Table):
            table_exp = dest_exp
        elif isinstance(dest_exp, exp.Schema):
            table_exp = dest_exp.this
            columns = dest_exp.expressions
        else:
            logger.info(
                "Only support insert in to table or schema, currently {}".format(type(dest_exp))
            )
    elif isinstance(ast, exp.Merge):
        dest_exp = ast.this
        if isinstance(dest_exp, exp.Table):
            table_exp = dest_exp
        else:
            logger.info("Only support merge into table, currently {}".format(type(dest_exp)))

    if not table_exp:
        return None

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


def get_scope(ast: Optional[exp.Expression]) -> Optional[Union[Scope, exp.Table]]:
    if not ast:
        return None
    if isinstance(ast, exp.Merge):
        merge_using = ast.args.get("using")
        if isinstance(merge_using, exp.Table):
            return merge_using
        elif isinstance(merge_using, exp.Expression):
            return build_scope(merge_using)

    return build_scope(ast)


def build_table_column_node(table_node: Node, column_name: str) -> Node:
    table_column_select_expression = exp.select(column_name).from_(table_node.expression)
    table_child = Node(
        name=column_name,
        expression=exp.to_identifier(column_name, quoted=False),
        generated_expression=table_column_select_expression,
        source_expression=table_column_select_expression,
        node_type=NodeType.COLUMN,
    )

    return table_child


def create_column_for_table(table_node: Node, column_name: str):
    table_node.add_child(build_table_column_node(table_node=table_node, column_name=column_name))


def populate_dest_children(
    dest_table: Node, schema: Schema, prefered_children: Optional[List[Node]] = None
):
    prefered_columns: List[str] = list(
        map(
            lambda x: x.name.sql() if isinstance(x.name, exp.Expression) else x.name,
            prefered_children or [],
        )
    )

    if isinstance(dest_table.expression, exp.Table):
        dest_schema_columns = schema.column_names(dest_table.expression)
        if len(dest_table.children) == 0:
            dest_columns = dest_schema_columns or prefered_columns

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


def link_source_to_dest(ast: exp.Expression, dest_table: Node, schema: Schema):
    if isinstance(ast, exp.Select) or isinstance(ast, exp.Create) or isinstance(ast, exp.Insert):
        if len(dest_table.downstreams) != 1:
            logger.debug(
                "Skip link source to dest. Dest table should contains only one SELECT downstream, currently; {}".format(
                    len(dest_table.downstreams)
                )
            )
            return
        elif dest_table.downstreams[0].node_type not in (NodeType.SELECT, NodeType.SUBQUERY):
            logger.info(
                "Skip link source to dest. Dest table downstream should be a select statement."
            )
            return

        select_downstream = dest_table.downstreams[0]
        if len(dest_table.children) > 0 and len(dest_table.children) != len(
            select_downstream.children
        ):
            raise Exception(
                "Can not build lineage for this statement. Missmatch number of columns."
                f"\n Number of dest children: {len(dest_table.children)}"
                f"\n Number of select downstream children: {len(select_downstream.children)}"
                f"\n dest children: {[str(c.name) for c in dest_table.children]}"
                f"\n select downstream children: {[str(c.name) for c in select_downstream.children]}"
            )

        populate_dest_children(
            dest_table=dest_table, schema=schema, prefered_children=select_downstream.children
        )
        for dest_child, select_child in zip(dest_table.children, select_downstream.children):
            dest_child.add_downstream(select_child)

    elif isinstance(ast, exp.Merge):
        merge_insert: Optional[exp.Insert] = None
        for when_statement in ast.find_all(exp.When):
            if not when_statement.args.get("matched", True) and isinstance(
                when_statement.args.get("then"), exp.Insert
            ):
                merge_insert = when_statement.args.get("then")

        merge_updates: List[exp.Update] = []
        for when_statement in ast.find_all(exp.When):
            when_then_statement = when_statement.args.get("then")
            if isinstance(when_then_statement, exp.Update):
                merge_updates.append(when_then_statement)

        dest_columns = []
        if merge_insert:
            if isinstance(merge_insert.this, exp.Tuple):
                for column in merge_insert.this.expressions:
                    if isinstance(column, exp.Column):
                        dest_columns.append(column.output_name)
            elif isinstance(dest_table.expression, exp.Table):
                dest_columns = list(schema.column_names(dest_table.expression))

        for merge_update in merge_updates:
            for eq in merge_update.find_all(exp.EQ):
                if isinstance(eq.this, exp.Column):
                    target_column = eq.this.output_name
                    if target_column and target_column not in dest_columns:
                        dest_columns.append(target_column)

        infer_dest_children = [
            build_table_column_node(table_node=dest_table, column_name=column)
            for column in dest_columns
        ]
        populate_dest_children(
            dest_table=dest_table, schema=schema, prefered_children=infer_dest_children
        )

        source_downstream = dest_table.downstreams[0]
        if merge_insert:
            merge_target_columns: List[str]
            if isinstance(merge_insert.this, exp.Tuple):
                merge_target_columns = list(
                    map(
                        lambda c: c.output_name,
                        filter(lambda c: isinstance(c, exp.Column), merge_insert.this.expressions),
                    )
                )
            elif isinstance(dest_table.expression, exp.Table):
                merge_target_columns = list(schema.column_names(dest_table.expression))

            for target_col_name, value in zip(
                merge_target_columns, merge_insert.expression.expressions
            ):
                target_child: Optional[Node] = dest_table.get_child_by_name(target_col_name)
                if not target_child:
                    continue

                if isinstance(value, exp.Expression):
                    for value_column in value.find_all(exp.Column):
                        source_child = source_downstream.get_child_by_name(value_column.output_name)
                        if source_child and not target_child.has_downstream(source_child):
                            target_child.add_downstream(source_child)

        for merge_update in merge_updates:
            for eq in merge_update.find_all(exp.EQ):
                if isinstance(eq.this, exp.Column):
                    target_col_name = eq.this.output_name
                    target_child = dest_table.get_child_by_name(target_col_name)

                    if not target_child:
                        continue

                    for value_column in eq.expression.find_all(exp.Column):
                        if value_column.table == source_downstream.name:
                            source_child = source_downstream.get_child_by_name(
                                value_column.output_name
                            )
                            if source_child and not target_child.has_downstream(source_child):
                                target_child.add_downstream(source_child)


def load_scope(
    scope: Union[Scope, exp.Table, None], root_node: Node, upstream: Node, schema: Schema
):
    create_node(
        root_node=root_node, upstream=upstream, node_name="dummy", scope=scope, schema=schema
    )


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
        elif not (
            isinstance(scope.expression, exp.Select) or isinstance(scope.expression, exp.Subquery)
        ):
            raise ValueError(
                "Expected a select or subquery statement, actually got {}.".format(scope.expression)
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
        elif isinstance(scope.expression, exp.Subquery):
            node_type = NodeType.SUBQUERY
            node_name = scope.expression.alias_or_name
            this_relation = scope.expression.this
            tmp_scope = get_scope(this_relation)
            if tmp_scope and isinstance(tmp_scope, Scope):
                scope = tmp_scope

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
            name=scope,
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

    schema = ensure_schema(schema, dialect=dialect)
    ast = qualify_ast(ast=ast, schema=schema, dialect=dialect)

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

    scp = get_scope(ast)
    if scp:
        load_scope(scp, root_node, dest_table or root_node, schema)

    # link output to dest table
    if dest_table:
        link_source_to_dest(ast=ast, dest_table=dest_table, schema=schema)

    return root_node
