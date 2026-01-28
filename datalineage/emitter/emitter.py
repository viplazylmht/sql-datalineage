from datalineage.node import Node

from abc import ABC, abstractmethod
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Emitter(ABC):
    """Emitter centralize multiple lineages metadata and synchronize
    them to a global metadata for analytic and visualization.
    """

    def __init__(self):
        self._global_metadata: Optional[Node] = None

    @abstractmethod
    def emit_lineage(self, emit_id: str, lineage_tree: Node) -> None:
        """Emit a datalineage to the global metadata. This method should
        update the cached global_metadata as well."""
        raise NotImplementedError
