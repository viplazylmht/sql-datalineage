from datalineage.node import Node
from datalineage.emitter.emitter import Emitter

import logging

logger = logging.getLogger(__name__)


class FileBasedEmitter(Emitter):
    """FileBsedEmitter allow to emit and retrieve the global lineage
    metadata back from file. Currently supports local file.
    """

    def __init__(self, file_path: str, overwrite=False):
        """
        Init FileBasedEmitter.

        file_path: str - path to file
        overwrite: bool - overwrite the original file (if exist). Default to append.
        """

        super().__init__()

        self._file_path = file_path
        self._overwrite = overwrite

    def emit_lineage(self, emit_id: str, lineage_tree: Node) -> None:
        """Emit a datalineage to the global metadata. This method should
        update the cached global_metadata as well."""
        raise NotImplementedError
