from typing import Union

from .renderer import Renderer
from .json_renderer import JsonRenderer
from .mermaid_renderer import MermaidRenderer

RENDERER_MAPPING = {
    "json": JsonRenderer,
    "mermaid": MermaidRenderer,
    "default": JsonRenderer,
}


def ensure_renderer(renderer: Union[Renderer, str], **kwargs) -> Renderer:
    if isinstance(renderer, Renderer):
        return renderer

    if not isinstance(renderer, str):
        raise ValueError("Renderer must be a str, currently {}".format(type(renderer)))

    renderer_clzz = RENDERER_MAPPING.get(renderer.lower())

    if renderer_clzz:
        return renderer_clzz(**kwargs)
    else:
        raise ValueError("Invalid renderer: {} is not a valid renderer type".format(renderer))
