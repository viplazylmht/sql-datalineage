import json
from datalineage.renderer.renderer import Renderer

from datalineage.node import Node


class JsonRenderer(Renderer):
    def __init__(self, pretty: bool = True):
        super().__init__()
        self._pretty: bool = False
        self.pretty = pretty

    @property
    def pretty(self) -> bool:
        return self._pretty

    @pretty.setter
    def pretty(self, v: bool):
        self._pretty = v

    def render(self, node: Node) -> str:
        json_content = node.to_json_dict()

        indent = None
        if self.pretty:
            indent = 4

        return json.dumps(json_content, indent=indent)
