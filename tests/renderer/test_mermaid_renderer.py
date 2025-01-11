import unittest
from sqlglot import exp, parse_one
from typing import Dict

from datalineage.renderer.mermaid_renderer import MermaidRenderer, MermaidType
from datalineage.node import ColumnNode, TableNode, SelectNode, Node


class TestmermaidRetriever(unittest.TestCase):
    """Testing Mermaid Retriever"""

    def setUp(self):
        self.table_node = TableNode(
            name="schema.table_a", expression=exp.to_table("schema.table_a")
        )
        self.table_age_column_node = ColumnNode(name="age", expression=exp.to_column("age"))
        self.table_gender_column_node = ColumnNode(
            name="gender", expression=exp.to_column("gender")
        )

        self.table_node.add_child(self.table_age_column_node)
        self.table_node.add_child(self.table_gender_column_node)

        self.select_node = SelectNode(
            name="_output_", expression=parse_one("select age, gender from schema.table_a")
        )
        self.select_age_column_node = ColumnNode(name="age", expression=exp.to_column("age"))
        self.select_gender_column_node = ColumnNode(
            name="gender", expression=exp.to_column("gender")
        )

        self.select_node.add_child(self.select_age_column_node)
        self.select_node.add_child(self.select_gender_column_node)

        self.select_node.add_downstream(self.table_node)
        self.select_age_column_node.add_downstream(self.table_age_column_node)
        self.select_gender_column_node.add_downstream(self.table_gender_column_node)

        return super().setUp()

    def test_get_node_id(self):
        base_node_ids: Dict[Node, int] = {}

        renderer = MermaidRenderer()

        self.assertEqual(
            renderer.get_node_id(base_node_ids, self.select_node),
            self.select_node.node_id,
        )
        self.assertEqual(
            renderer.get_node_id(base_node_ids, self.select_node),
            self.select_node.node_id,
        )
        self.assertEqual(
            renderer.get_node_id(base_node_ids, self.table_gender_column_node),
            self.table_gender_column_node.node_id,
        )
        self.assertEqual(
            renderer.get_node_id(base_node_ids, self.table_gender_column_node),
            self.table_gender_column_node.node_id,
        )

    def test_render_source(self):
        self.assertEqual(
            MermaidRenderer(output_type=MermaidType.SOURCE).render(self.select_node),
            """%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
graph LR
subgraph 11721865190390553753 ["Table: schema.table_a"]
9995307758889343154["age"]
11573945534907247447["gender"]
end

subgraph 15216115208654443094 ["Select: _output_"]
1561712693222949605["age"]
5034224727634001037["gender"]
end
9995307758889343154 --> 1561712693222949605
11573945534907247447 --> 5034224727634001037
""",
        )

    def test_render_html(self):
        self.assertEqual(
            MermaidRenderer(output_type=MermaidType.HTML).render(self.select_node),
            """<!doctype html>
        <html lang="en">
        <head>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet"/>
        </head>
        <body>
            <pre class="mermaid">
                %%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
graph LR
subgraph 11721865190390553753 ["Table: schema.table_a"]
9995307758889343154["age"]
11573945534907247447["gender"]
end

subgraph 15216115208654443094 ["Select: _output_"]
1561712693222949605["age"]
5034224727634001037["gender"]
end
9995307758889343154 --> 1561712693222949605
11573945534907247447 --> 5034224727634001037

            </pre>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
                mermaid.initialize({ startOnLoad: false });

                await mermaid.run({
                    querySelector: '.mermaid',
                });
            </script>
        </body>
        </html>""",
        )


if __name__ == "__main__":
    unittest.main()
