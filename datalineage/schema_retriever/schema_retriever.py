from abc import ABC, abstractmethod
from copy import deepcopy

from sqlglot import exp
from sqlglot.schema import Schema, ensure_schema
from typing import List, Dict, Optional, Union
import logging

logger = logging.getLogger(__name__)


class SchemaRetriever(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def retrieve_table_schema(self, table: exp.Table) -> Optional[Dict]:
        return NotImplemented

    def retrieve_schema(
        self,
        base_schema: Optional[Union[Schema, Dict]],
        tables: List[Union[exp.Table, str]],
        dialect: Optional[str] = None,
        force_refresh: bool = True,
        copy=False,
    ) -> Schema:
        schema: Schema
        if isinstance(base_schema, Schema) and copy:
            schema = deepcopy(base_schema)
        else:
            schema = ensure_schema(base_schema, dialect=dialect)

        for table in tables:
            if isinstance(table, str):
                table = exp.to_table(table, dialect=dialect)
            table_columns = schema.column_names(table=table, dialect=dialect)

            if not table_columns or force_refresh:
                column_mapping: Optional[Dict] = None
                try:
                    column_mapping = self.retrieve_table_schema(table)
                except Exception as e:
                    logger.info(
                        msg="Failed to retrieving columns schema for table {}. Error: {}".format(
                            table.sql(), str(e)
                        )
                    )

                if column_mapping:
                    schema.add_table(table=table, column_mapping=column_mapping, dialect=dialect)

        return schema
