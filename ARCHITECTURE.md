# Architecture of SQL Data Lineage

This document provides a detailed overview of the architectural design, key components, and data flow of the `sql-datalineage` project.

## Overview

`sql-datalineage` is a Python library and CLI tool designed to parse SQL queries and build comprehensive column-level data lineage graphs. It understands how data flows across sources (Tables), intermediate transformations (CTEs, Subqueries, Unions), and targets (Select outputs, Create/Insert tables).

At its core, the project leverages [sqlglot](https://github.com/tobymao/sqlglot), a powerful SQL parser and transpiler, to parse SQL statements into Abstract Syntax Trees (ASTs), qualify column scopes, and resolve schemas.

## Core Modules

The architecture is composed of several decoupled modules:

### 1. `datalineage.lineage` (The Core Engine)
This is the primary entry point for generating lineage. The core logic inside `lineage.py` performs the following steps:
1. **Parse & Qualify:** Takes a raw SQL string, dialect, and schema, then uses `sqlglot` to parse the query and qualify the AST. `qualify` automatically resolves and infers column sources.
2. **Scope Building:** Constructs a `sqlglot.optimizer.scope.Scope` hierarchy representing the dependencies of subqueries, CTEs, and base tables.
3. **Node Graph Construction:** Traverses the scopes recursively (`load_scope` and `create_node`) to instantiate a Directed Acyclic Graph (DAG) composed of `Node` objects representing operations, expressions, and columns.
4. **Target Resolution:** Resolves potential destination tables (for `INSERT`, `CREATE`, or `MERGE` statements) and links the upstream output columns to destination columns.

### 2. `datalineage.node` (Graph Object Model)
This module defines the DAG structure using an object-oriented approach.
- **Base `Node` Class:** Every object in the graph inherits from `Node`. A `Node` contains references to its `children`, `upstreams`, and `downstreams`. It provides powerful traversal methods like `walk()`, `upstream_walk()`, `downstream_walk()`, and `reversed_walk()`.
- **Node Types:**
  - `TableNode`: Represents a base table.
  - `ColumnNode`: Represents a column within a scope or table.
  - `SelectNode`: Represents a `SELECT` statement.
  - `CTENode`: Represents a Common Table Expression.
  - `SubqueryNode`: Represents a nested query.
  - `UnionNode` / `UnionAllNode`: Represents `UNION` and `UNION ALL` statements.
  - `UnknownNode`: Fallback for unrecognized scopes.
- **Visitor Pattern:** Includes `NodeVisitor` base class allowing custom logic to be applied over graph nodes without modifying the node classes.

### 3. `datalineage.renderer` (Visualization)
Renderers are responsible for translating the internal node graph into visual or serialized output formats.
- **`MermaidRenderer`:** Traverses the graph to generate Mermaid flowchart syntax (`graph LR`). It clusters columns under their parent nodes (represented as Mermaid subgraphs) and links column nodes to show direct data flow. It can return raw Mermaid strings or render directly to an IPython/Jupyter HTML output.
- **`JsonRenderer`:** Dumps the node graph recursively into a standardized JSON format.
- **`Renderer` (Interface):** New formats can easily be added by subclassing this interface.

### 4. `datalineage.schema_retriever` (Schema Resolution)
For accurate lineage, `sql-datalineage` needs to know the source table schemas (to expand `SELECT *`, or resolve unqualified columns).
- **`SchemaRetriever`**: Base class handling ThreadPool-based multi-threaded schema retrieval for speed.
- **`StaticSchemaRetriever`**: Loads statically provided dictionary-based schemas.
- **`SQLAlchemySchemaRetriever`**: Introspects live database engines via SQLAlchemy's `inspect` API to fetch real-time schemas on the fly.

### 5. `datalineage.visitor` (Tree Traversal Logic)
Provides concrete implementations of the `NodeVisitor` pattern.
- **`PrettyNameVisitor`:** Formats the node into an easily readable string based on its node type (e.g., `Table: customer`, `Select Statement: _output_`).

### 6. `datalineage.serializer` (Serialization)
Provides `Serializer` implementation that leverages Python's `pickle` library. This is useful for saving and loading complex graph states during intermediate processing or caching.

### 7. `cli.py` (Command Line Interface)
Provides an interactive CLI powered by `click`. It takes SQL files (`-i`) and optional schema files (`--schema-path`), calls `lineage()` from `datalineage.lineage`, and utilizes a renderer (JSON or Mermaid) to write output to the terminal or a file (`-o`).

## Graph Traversal and Data Flow

The node structure naturally builds a graph connecting different contexts.
For example, for the query:
```sql
SELECT id, name FROM (SELECT id, name FROM catalog.schema1.customer) data
```
The internal DAG is structured as follows:
1. `TableNode: "catalog"."schema1"."customer" AS "customer"`
   - Child `ColumnNode: id`
   - Child `ColumnNode: name`
2. `SubqueryNode: data`
   - Child `ColumnNode: id` (has upstream `TableNode.id`)
   - Child `ColumnNode: name` (has upstream `TableNode.name`)
3. `SelectNode: _output_`
   - Child `ColumnNode: id` (has upstream `SubqueryNode.id`)
   - Child `ColumnNode: name` (has upstream `SubqueryNode.name`)

Edges represent the direct flow of column-level lineage. The `Renderer` layer uses these upstream/downstream connections and nested children logic to output visuals mapping this structure accurately.

## Summary

The `sql-datalineage` library exhibits a robust architecture where SQL parsing (`sqlglot`), schema resolution, object-graph mapping, and graph rendering are heavily decoupled. This allows seamless integration whether used interactively via CLI, programmatically inside pipelines, or dynamically alongside live data warehouses with SQLAlchemy.
