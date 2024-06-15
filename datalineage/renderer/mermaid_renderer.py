from enum import Enum
from typing import List
from sqlglot import exp

from datalineage.node import Node, NodeType
from datalineage.renderer.renderer import Renderer


class MermaidType(str, Enum):
    SOURCE = "SOURCE"
    SVG = "SVG"


class MermaidRenderer(Renderer):
    DEFAULT_CONFIGURATION = [
        """%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%""",
    ]

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
                result.append('{}["{}"]'.format(id(child), child.name.replace('"', "")))
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
        elif self.output_type == MermaidType.SVG:
            # TODO: render mermaid_source to SVG
            pass

        return result
