from typing import Optional
from datalineage.schema_retriever.schema_retriever import SchemaRetriever


class BaseContext:
    def __init__(self):
        self._schema_retriever: Optional[SchemaRetriever] = None
        self.output

    def _init_schema_retriever(self) -> SchemaRetriever:
        return NotImplemented

    @property
    def schema_retriever(self) -> SchemaRetriever:
        if not self._schema_retriever:
            self._schema_retriever = self._init_schema_retriever()

        return self._schema_retriever
