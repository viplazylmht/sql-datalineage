from enum import Enum
from typing import List
from sqlglot import exp
from jinja2 import Template
from IPython.display import HTML, display

from datalineage.node import Node, NodeType
from datalineage.renderer.renderer import Renderer


class MermaidType(str, Enum):
    SOURCE = "SOURCE"
    HTML = "HTML"


class MermaidRenderer(Renderer):
    DEFAULT_CONFIGURATION = [
        """%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%""",
    ]

    _MERMAID_HTML_TEMPLATE = """
        <!doctype html>
        <html lang="en">
        <head>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet"/>
        </head>
        <body>
            <pre class="mermaid">
                {{ mermaid_source }}
            </pre>
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
                mermaid.initialize({ startOnLoad: false });

                await mermaid.run({
                    querySelector: '.mermaid',
                });
            </script>
        </body>
        </html>
    """

    def __init__(
        self,
        output_type: MermaidType = MermaidType.SOURCE,
        configuration: List[str] = DEFAULT_CONFIGURATION,
    ):
        super().__init__()

        self.output_type = output_type
        self.configuration = configuration

    def _template_mermaid_flowchart(self, node: Node) -> str:
        result = self.configuration + [
            "graph LR",
        ]
        for n in node.reversed_walk():
            if len(n.children) == 0:
                continue

            replaced_name = self.remove_quote(str(n.name))

            # each primary node is a subgraph
            node_type = n.node_type or NodeType.UNKNOWN
            result.append('subgraph {} ["{}: {}"]'.format(id(n), node_type.value, replaced_name))
            for child in n.children:
                result.append('{}["{}"]'.format(id(child), str(child.name).replace('"', "")))
            result.append("end")

            # define links between node
            for child in n.children:
                if isinstance(child.expression, exp.Func):
                    result.append(
                        '{}_exp[["{}"]] ----- {}'.format(
                            id(child),
                            self.remove_quote(child.expression.sql()),
                            id(child),
                        )
                    )
                for d in child.downstreams:
                    result.append(f"{id(d)} --> {id(child)}")
            result.append("")

        return "\n".join(result)

    def render(self, node: Node) -> str:
        mermaid_source = self._template_mermaid_flowchart(node)

        result = ""
        if self.output_type == MermaidType.SOURCE:
            result = mermaid_source
        elif self.output_type == MermaidType.HTML:
            rendered_template = Template(self._MERMAID_HTML_TEMPLATE).render(
                mermaid_source=mermaid_source
            )

            display(HTML(rendered_template))
            result = rendered_template

        return result
