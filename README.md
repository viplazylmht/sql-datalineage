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
$ cat query.sql
with cte1 as (
    select id, name, phone, address from catalog.schema1.customer
    where name like 'duy%'
)
, tmp_cte as (
select id, name, age, phone, customer_job from catalog.schema1.user_demographics
)
, cte2 as (
select id, name, age, phone, customer_job job from tmp_cte
)
, cte3 as (
select id, name, age, phone, job from catalog.schema1.tbl_cte3
)
select * from (
select t1.*, concat(t1.name, t2.name) as full_name, max(age) as max_age, (SELECT MAX(id) AS max_id FROM catalog.schema1.customer) as maxid
from cte1 t1 left join cte2 t2 on t1.phone = t2.phone
group by t1.id, concat(t1.name, t2.name)
having max(age) > 10
) where id < 5

$ cat schema.json
{
  "catalog": {
      "schema1": {
          "customer": {
              "id": "INTEGER",
              "name": "STRING",
              "phone": "STRING",
              "address": "STRING",
              "location": "STRING"
          },
          "user_demographics": {
              "id": "INTEGER",
              "name": "STRING",
              "age": "STRING",
              "phone": "STRING",
              "customer_job": "STRING",
              "parent": "STRING"
          },
          "tbl_cte3": {
              "id": "INTEGER",
              "name": "STRING",
              "age": "STRING",
              "phone": "STRING",
              "address": "STRING",
              "job": "STRING"
          }
      }
  }
}

$ datalineage -i example/test-query.sql --schema-path example/test-schema.json -r mermaid

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
> Output of the above command are truncated. You can
> optional save the result of command to file using
> `-o` setting.

> [!NOTE]
> Currently, the above result are dynamically generated,
> so each run will have different IDs. Don't worry, the
> lineage is deterministic.


You can preview the above result using [Mermaid Live Editor](https://mermaid.live/view#pako:eNqdV1Fv2zYQ_iuCgAAdkDoUJVKUHwYEWd_WDWjyMKwqBFqibW2ypErU1sDwf--RslLzQgfD_GSRH8m77767I49h2VUqXIc3N8e6rfU6OObhtun-Lfdy0Hlovyu1lVOjP6m2UoMazGgequbvPDydgtPNTd7uBtnvg18_5e04beYPmlAieJQkImU0-JyHT3LTqHVQSi2bbrcay706yGhVTqPuDmoI7h-D5X8efsnblw3SiAtYX1fuMM9SDsOtPCh3QiQ8gYl-37WXM4RlJIoozMiqGtQ4ou1iYlY1HRhYd62dBIfz1usTpYnx6eHpA3ikVWSs1xGyQyQ-uzOSEL_dNKUeu82SSCTIbmuaQ1Hw_v3PgXM4IssFGDMQaWgHMAdxh3YAq67Qk0T8jZBPoxqKSh06u6wuR8Peq0FEQUITH5mM-snMeGTUIXd4PKbCTzJPY7Ni0WDxV7dBS1Ornl4OqtVv6yOLU_6iD33oC9CIlcj8Fx0sBPG5xq2MX7sGxFOfa2lmHUCuxcwuID7XXBEZit0IG8sQ2UgCYCMi3QWYoxH7LsAYjYLwA7DYfkVlKXGSkFqGqUtKzLzFIxNE-HUjmF831AbJpxtu89nPqWHQddgYhKKMOAXTULQxgHEUdgSgL2FbGERx5YmfU0ZNlv__Yp2JNLH8uXzDMKE-McOEEN58zIC4-EqxhlXcltb_VKwZiYXVyaNqVAkd7rGUjRwCAH6d1PDs7kxSW2oP8ltx9uEyoPN8ob71nwH08f6PdwsLq7r6CeBfgGj4BQ4e0XMZiwXgLSJECGv32dB1UHwtCMr5mT4s7zM_iG7CCSEZ98qYRYImV3ojI8y22u3UNIUnZeYUM5R50sYGEeY8bM5dCtUDcAg1SwTgTmMzXeoCcHYR9U5nB-spcm6J6MPvvz3cP73T0cq4eQvVxP7xRHZe95alrwCQ128DgMdLacHhwKfvbAtFRQuVAAcwpwCqETG9UlZFxi_Tpegm3U-6cCVBCff0Yxal1FtXWcRiv_CSNPZfyhiD3IivCY_BlYdT4RWeXTnX8WvCMzJzg2EcQhmEZAOuoUxCAHbZyqzMkHTjy2Zow_8DsLiLBHEBOHuMsgvtYHtDeBtCSTrIuoKb_TFvA7iva6jgar66l88bNfRTCxf4vD0BWE66e3xuy3Cth0ndhkM37fbLx9RXUqtfagk6OSyDvWz_7Dr43MpmfAF9qGrdDS-DTSfhwRCuj6F-7s0jY1ePGo4ru3Zb78z4NDQwvNe6H9d3d2Z6tav1ftqsyu5wN9aVeYXs_8n4HadcSBoruCBIFsdVuYHauaVJtK1SElEJT5HbUNnzP84vGvuwOX0HCJN90Q), here is the result:

![readme_example](https://raw.github.com/viplazylmht/sql-datalineage/master/docs/readme_example.svg)



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
