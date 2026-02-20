from abc import ABC, abstractmethod

from concurrent.futures import ThreadPoolExecutor

from sqlglot import exp
from sqlglot.schema import Schema, ensure_schema
from typing import List, Dict, Optional, Union, Iterable
import logging

from threading import Lock

logger = logging.getLogger(__name__)


class SchemaRetriever(ABC):
    def __init__(self, schema: Optional[Union[Schema, Dict]], dialect: Optional[str]):
        self._schema = ensure_schema(schema=schema, dialect=dialect)
        self._dialect = dialect
        self._lock = Lock()

    @property
    def schema(self) -> Schema:
        with self._lock:
            return self._schema

    @property
    def dialect(self) -> Optional[str]:
        return self._dialect

    @abstractmethod
    def retrieve_table_schema(self, table: exp.Table) -> Optional[Dict]:
        return NotImplemented

    def retrieve_ignoring_errors(self, table: exp.Table) -> Optional[Dict]:
        try:
            return self.retrieve_table_schema(table)
        except Exception as e:
            logger.info(
                msg="Failed to retrieving columns schema for table {}. Error: {}".format(
                    table.sql(), str(e)
                )
            )

        return None

    def retrieve_schema(self, tables: Iterable[Union[exp.Table, str]]) -> Schema:
        retrieval_tasks: List[exp.Table] = []
        for table in tables:
            if isinstance(table, str):
                table = exp.to_table(table, dialect=self.dialect)
            retrieval_tasks.append(table)

        if not retrieval_tasks:
            return self.schema

        column_mappings = []
        with ThreadPoolExecutor() as executor:
            column_mappings = executor.map(self.retrieve_ignoring_errors, retrieval_tasks)

        with self._lock:
            for table, column_mapping in zip(retrieval_tasks, column_mappings):
                if column_mapping:
                    self._schema.add_table(
                        table=table, column_mapping=column_mapping, dialect=self.dialect
                    )

        return self.schema
