from typing import Dict
from datalineage.renderer.renderer import Renderer

from datalineage.node import Node


class JsonRenderer(Renderer):
    def __init__(self):
        super().__init__()

    def render(self, node: Node) -> Dict:
        return node.to_json_dict()
