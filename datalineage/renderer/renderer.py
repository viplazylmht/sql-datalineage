from abc import ABC, abstractmethod
from typing import Any
import re
from datalineage.node import Node


class Renderer(ABC):
    """
    Render column level lineage from a node
    """

    def __init__(self):
        if self.__class__.__name__ == "Renderer":
            raise Exception(
                "Cannot instantiate abstract class Renderer, you need to instantiate one of its subclasses."
            )

    @abstractmethod
    def render(self, node: Node) -> Any:
        raise ModuleNotFoundError

    @staticmethod
    def remove_quote(string: str) -> str:
        return re.sub(r'["]', "", string)
