<div align="center">
<br>
<h1>SQL Data Lineage</h1>
<p>
  <a href="https://github.com/viplazylmht/sql-datalineage/actions/workflows/python-package.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/viplazylmht/sql-datalineage/python-package.yml">
  </a>
  <a href="https://github.com/viplazylmht/sql-datalineage/actions/workflows/python-publish.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/viplazylmht/sql-datalineage/python-publish.yml?label=publish">
  </a>
  <a href="https://pypi.org/project/sql-datalineage">
    <img src="https://img.shields.io/pypi/v/sql-datalineage?color=cyan">
  </a>
</p>
</div>

Introducing SQL Data Lineage, a powerful package designed to simplify SQL query analysis. This versatile tool parses data lineage from individual SQL queries or builds comprehensive lineage from multiple queries. It offers both an interactive command-line interface and programmatic integration, making it easy to incorporate into your Python projects.

SQL Data Lineage performs detailed column-level analysis, tracing data flows step-by-step through tables, CTEs, subqueries, and more. It generates user-friendly lineage graphs that clearly show how columns move and transform across SQL components.

You can easily enhance your lineage insights by retrieving and customizing metadata to fit your specific requirements.

We welcome and encourage contributions to the SQL Data Lineage project!


# Installation
```bash
pip install sql-datalineage
```

# Usage

## CLI usage

Show help of CLI commands.
```bash
datalineage --help
```

Generate data lineage of a sql file, output type is mermaid.
```bash
$> datalineage -i docs/example/test-query.sql --schema-path docs/example/test-schema.json -r mermaid

%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
graph LR
subgraph 2420861448752 ["Table: catalog.schema1.customer AS customer"]
2420861447168["id"]
2420861446976["name"]
2420861448464["phone"]
2420860590112["address"]
2420861446304["location"]
end

subgraph 2420861448224 ["CTE: cte1 AS t1"]
2420861448848["id"]
2420861449040["name"]
2420861448272["phone"]
2420861449184["address"]
end
2420861447168 --> 2420861448848
2420861446976 --> 2420861449040
2420861448464 --> 2420861448272
2420860590112 --> 2420861449184

....
```

> [!TIP]
> The output of the above command is truncated. You
> can optionally save the command's result to a file
> using the `-o` option.
> ```bash
> datalineage -i /docs/example/test-query.sql --schema-path docs/example/test-schema.json -o docs/example/output.mermaid -r mermaid
> ```

> [!NOTE]
> Currently, the results are generated dynamically, so
> each run will produce different IDs. However, rest
> assured that the lineage remains deterministic.


You can preview the above result using [Mermaid Live Editor](https://mermaid.live/view#pako:eNqdV1Fv2zYQ_iuCgAAdkDoUJVKUHwYEWd_WDWjyMKwqBFqibW2ypErU1sDwf--RslLzQgfD_GSRH8m77767I49h2VUqXIc3N8e6rfU6OObhtun-Lfdy0Hlovyu1lVOjP6m2UoMazGgequbvPDydgtPNTd7uBtnvg18_5e04beYPmlAieJQkImU0-JyHT3LTqHVQSi2bbrcay706yGhVTqPuDmoI7h-D5X8efsnblw3SiAtYX1fuMM9SDsOtPCh3QiQ8gYl-37WXM4RlJIoozMiqGtQ4ou1iYlY1HRhYd62dBIfz1usTpYnx6eHpA3ikVWSs1xGyQyQ-uzOSEL_dNKUeu82SSCTIbmuaQ1Hw_v3PgXM4IssFGDMQaWgHMAdxh3YAq67Qk0T8jZBPoxqKSh06u6wuR8Peq0FEQUITH5mM-snMeGTUIXd4PKbCTzJPY7Ni0WDxV7dBS1Ornl4OqtVv6yOLU_6iD33oC9CIlcj8Fx0sBPG5xq2MX7sGxFOfa2lmHUCuxcwuID7XXBEZit0IG8sQ2UgCYCMi3QWYoxH7LsAYjYLwA7DYfkVlKXGSkFqGqUtKzLzFIxNE-HUjmF831AbJpxtu89nPqWHQddgYhKKMOAXTULQxgHEUdgSgL2FbGERx5YmfU0ZNlv__Yp2JNLH8uXzDMKE-McOEEN58zIC4-EqxhlXcltb_VKwZiYXVyaNqVAkd7rGUjRwCAH6d1PDs7kxSW2oP8ltx9uEyoPN8ob71nwH08f6PdwsLq7r6CeBfgGj4BQ4e0XMZiwXgLSJECGv32dB1UHwtCMr5mT4s7zM_iG7CCSEZ98qYRYImV3ojI8y22u3UNIUnZeYUM5R50sYGEeY8bM5dCtUDcAg1SwTgTmMzXeoCcHYR9U5nB-spcm6J6MPvvz3cP73T0cq4eQvVxP7xRHZe95alrwCQ128DgMdLacHhwKfvbAtFRQuVAAcwpwCqETG9UlZFxi_Tpegm3U-6cCVBCff0Yxal1FtXWcRiv_CSNPZfyhiD3IivCY_BlYdT4RWeXTnX8WvCMzJzg2EcQhmEZAOuoUxCAHbZyqzMkHTjy2Zow_8DsLiLBHEBOHuMsgvtYHtDeBtCSTrIuoKb_TFvA7iva6jgar66l88bNfRTCxf4vD0BWE66e3xuy3Cth0ndhkM37fbLx9RXUqtfagk6OSyDvWz_7Dr43MpmfAF9qGrdDS-DTSfhwRCuj6F-7s0jY1ePGo4ru3Zb78z4NDQwvNe6H9d3d2Z6tav1ftqsyu5wN9aVeYXs_8n4HadcSBoruCBIFsdVuYHauaVJtK1SElEJT5HbUNnzP84vGvuwOX0HCJN90Q), here is the result:

![readme_example](https://raw.github.com/viplazylmht/sql-datalineage/master/docs/img/readme_example.svg)


## Interactive usage

You can import datalineage into your project and generate the lineage tree directly.

```python
>>> from datalineage.lineage import lineage
>>> sql = """select  
  id, name, phone, address
  from (
    select id, name, phone, address,
    row_number() over(partition by phone order by name) as rn    
    from `catalog.schema1.customer`) data
  where data.rn = 1
"""
>>> schema = None # we will infer the schema of table when no schema are provided
>>> dialect = "bigquery"
>>> tree = lineage(sql, dialect, schema)
>>> tree
Node<{"name": "myroot", "expression": "ANCHOR",...
```

You can traversal and print out the lineage tree in this way:
```python
>>> def print_node(node):
>>>     print("Node:", node.name)
>>>     list(map(lambda c: print("Column:", c.name), node.children))
>>> for node in tree.walk():
...     print_node(node)
... 
Node: myroot
Node: _output_
Column: id
Column: name
Column: phone
Column: address
Node: data
Column: id
Column: name
Column: phone
Column: address
Column: rn
Node: "catalog"."schema1"."customer" AS "customer"
Column: id
Column: name
Column: phone
Column: address
```

Or you can render the tree to a format you like, for example, mermaid.
```python
>>> from datalineage.renderer import MermaidRenderer
>>> renderer = MermaidRenderer()
>>> print(renderer.render(tree))
%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
graph LR
subgraph 1434247920720 ["Table: catalog.schema1.customer AS customer"]
1434247920624["id"]
1434247921104["name"]
1434247919568["phone"]
1434247921200["address"]
end

subgraph 1434247919280 ["Subquery: data"]
1434247920816["id"]
1434247919856["name"]
1434247917696["phone"]
1434247917744["address"]
1434247918224["rn"]
end
1434247920624 --> 1434247920816
1434247921104 --> 1434247919856
1434247919568 --> 1434247917696
1434247921200 --> 1434247917744
1434247919568 --> 1434247918224
1434247921104 --> 1434247918224

subgraph 1434247918032 ["Select: _output_"]
1434247921392["id"]
1434247921344["name"]
1434247921152["phone"]
1434247920912["address"]
end
1434247920816 --> 1434247921392
1434247919856 --> 1434247921344
1434247917696 --> 1434247921152
1434247917744 --> 1434247920912
>>>
```
> [!TIP]
> You can render to json format using `datalineage.renderer.JsonRenderer` class, or customize your own renderer.
> 
> Here is the flow-chart of the above result:
> ```mermaid
> %%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
> graph LR
> subgraph 1434247920720 ["Table: catalog.schema1.customer AS customer"]
> 1434247920624["id"]
> 1434247921104["name"]
> 1434247919568["phone"]
> 1434247921200["address"]
> end
> 
> subgraph 1434247919280 ["Subquery: data"]
> 1434247920816["id"]
> 1434247919856["name"]
> 1434247917696["phone"]
> 1434247917744["address"]
> 1434247918224["rn"]
> end
> 1434247920624 --> 1434247920816
> 1434247921104 --> 1434247919856
> 1434247919568 --> 1434247917696
> 1434247921200 --> 1434247917744
> 1434247919568 --> 1434247918224
> 1434247921104 --> 1434247918224
> 
> subgraph 1434247918032 ["Select: _output_"]
> 1434247921392["id"]
> 1434247921344["name"]
> 1434247921152["phone"]
> 1434247920912["address"]
> end
> 1434247920816 --> 1434247921392
> 1434247919856 --> 1434247921344
> 1434247917696 --> 1434247921152
> 1434247917744 --> 1434247920912
> ```


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
