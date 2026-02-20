import unittest
from sqlglot import exp
from sqlglot.schema import Schema
from typing import List, Optional, Dict, Set, Union

from datalineage.schema_retriever.schema_retriever import SchemaRetriever
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
import asyncio
from threading import Thread


class MockSchemaRetriever(SchemaRetriever):
    def __init__(self):
        super().__init__(schema=None, dialect=None)

    def retrieve_table_schema(self, table: exp.Table) -> Optional[Dict]:
        return {"id": "int", "message": "text", "send_on": "timestamp"}


class TestSchemaRetrieverBase(unittest.TestCase):
    """Base class to allow testing on subclass."""

    def validate_column_names(
        self, schema: Schema, table: Union[exp.Table, str], dialect: str, column_names: Set[str]
    ):
        with self.subTest(
            "test set of column names of table {} = {}".format(str(table), column_names)
        ):
            self.assertEqual(set(schema.column_names(table=table, dialect=dialect)), column_names)

    def validate_column_type(
        self,
        schema: Schema,
        table: Union[exp.Table, str],
        dialect: str,
        column: str,
        column_type: exp.DataType,
    ):
        with self.subTest(
            "test data type of column {} in table {} = {}".format(column, str(table), column_type)
        ):
            self.assertEqual(
                schema.get_column_type(table=table, column=column, dialect=dialect),
                column_type,
            )


class TestSchemaRetriever(unittest.TestCase):
    async def run_retriever_in_event_loop(
        self, mock_retriever: SchemaRetriever, tables: List[exp.Table]
    ):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, mock_retriever.retrieve_schema, tables)

    def test_thread_safety_thread_pool(self):
        mock_retriever = MockSchemaRetriever()
        tables = [exp.to_table("table_{}".format(i)) for i in range(100)]

        # test can run in thread pool without error or deadlock
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(mock_retriever.retrieve_schema, tables) for _ in range(20)]

            _, not_done = wait(futures, timeout=5, return_when=ALL_COMPLETED)
            self.assertTrue(len(not_done) == 0, "Thread safety test timed out (possible deadlock)")

    def test_thread_safety_asyncio_parallel(self):
        # test can run in two asyncio event loop without error or deadlock
        mock_retriever = MockSchemaRetriever()
        tables = [exp.to_table("table_{}".format(i)) for i in range(100)]

        thread1 = Thread(
            target=lambda: asyncio.run(
                self.run_retriever_in_event_loop(mock_retriever=mock_retriever, tables=tables)
            ),
            name="Thread-Test-1",
        )
        thread2 = Thread(
            target=lambda: asyncio.run(
                self.run_retriever_in_event_loop(mock_retriever=mock_retriever, tables=tables)
            ),
            name="Thread-Test-2",
        )

        thread1.start()
        thread2.start()

        thread1.join(timeout=5)
        thread2.join(timeout=5)

        alive_thread_name = ",".join([t.name for t in [thread1, thread2] if t.is_alive()])

        self.assertTrue(
            alive_thread_name == "",
            "Thread safety test timed out (possible deadlock), alive threads: {}".format(
                alive_thread_name
            ),
        )

    def test_thread_safety_asyncio_sequential(self):
        # test can create retriever in a event loop and run retrieve_schema in another event loop without error or deadlock
        async def create_retriever_and_run_in_event_loop():
            retriever = MockSchemaRetriever()
            tables = [exp.to_table("table_{}".format(i)) for i in range(100)]

            thread = Thread(
                target=lambda: asyncio.run(
                    self.run_retriever_in_event_loop(mock_retriever=retriever, tables=tables)
                ),
                name="Thread-Test-1",
            )
            thread.start()
            thread.join(timeout=5)

            self.assertFalse(thread.is_alive(), "Thread safety test timed out (possible deadlock)")

        asyncio.run(create_retriever_and_run_in_event_loop())


if __name__ == "__main__":
    unittest.main()
