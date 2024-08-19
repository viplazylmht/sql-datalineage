<div align="center">
<br>
<h1>SQL Data Lineage</h1>
</div>

[![Test and Lint](https://github.com/viplazylmht/sql-datalineage/actions/workflows/python-package.yml/badge.svg)](https://github.com/viplazylmht/sql-datalineage/actions/workflows/python-package.yml)
[![Publish Python Package to PyPI](https://github.com/viplazylmht/sql-datalineage/actions/workflows/python-publish.yml/badge.svg)](https://github.com/viplazylmht/sql-datalineage/actions/workflows/python-publish.yml)
![PyPI - Version](https://img.shields.io/pypi/v/sql-datalineage?color=cyan)


Introducing SQL Data Lineage, a powerful package designed to simplify SQL query analysis. This versatile tool parses data lineage from individual SQL queries or builds comprehensive lineage from multiple queries. It offers both an interactive command-line interface and programmatic integration, making it easy to incorporate into your Python projects.

SQL Data Lineage performs detailed column-level analysis, tracing data flows step-by-step through tables, CTEs, subqueries, and more. It generates user-friendly lineage graphs that clearly show how columns move and transform across SQL components.

You can easily enhance your lineage insights by retrieving and customizing metadata to fit your specific requirements.

We welcome and encourage contributions to the SQL Data Lineage project!


# Install
```bash
pip install sql-datalineage
```

# Usage
```bash
datalineage --help
```

# Contribution

### Setup Environment
```bash
make install-dev
```

### Run Lint
```bash
make style
```

### Run Tests
```bash
make test
```
