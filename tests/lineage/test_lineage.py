import unittest
import json
import pathlib
from pydantic import BaseModel, Field
from typing import Optional, List
import yaml

from datalineage.lineage import lineage
from datalineage.util import safe_read


class ConfigurationModel(BaseModel):
    path: str = Field(description="Path from pwd")
    input_path: str = Field(description="input path")
    output_path: str = Field(description="output path")
    schema_path: str = Field(description="path to schema json file.")
    dialect: Optional[str] = Field(description="sqlglot dialect", default=None)

    # TODO: allow output_type to be mermaid
    output_type: str = Field(
        description="renderer type. Available options is json and mermaid, default to json",
        default="json",
    )


"""Test lineage with configuration, defined in the lineage_conf.yaml file.
"""


class TestLineage(unittest.TestCase):
    PWD = pathlib.Path(__file__).parent.resolve()
    CONF_PATH = PWD / "lineage_conf.yaml"

    def setUp(self) -> None:
        super().setUp()

        self.configurations: List[ConfigurationModel] = []

        with self.subTest("test load configuration from path"):
            data = safe_read(str(self.CONF_PATH))
            self.assertIsNotNone(data)

            conf: List = yaml.safe_load(data or "")
            self.assertIsInstance(conf, list)
            self.assertTrue(len(conf) > 0)

            self.configurations = list(map(ConfigurationModel.model_validate, conf))

    def validate_lineage_equal(
        self, test_name: str, sql: str, dialect: str, schema: dict, output_str: str
    ):
        with self.subTest("Test lineage equal: {}".format(test_name)):
            generated_lineage = lineage(sql, dialect, schema)
            self.assertEqual(json.dumps(generated_lineage.to_json_dict(), indent=4), output_str)

            another_generated_lineage = lineage(sql, dialect, schema)
            self.assertEqual(
                generated_lineage,
                another_generated_lineage,
                "FLAKY: lineage generates inconsistent results!",
            )

    def test_lineage(self):
        print("test lineage")
        for conf in self.configurations:
            path = self.PWD / conf.path
            input_str = safe_read(path / conf.input_path)
            output_str = safe_read(path / conf.output_path)
            schema = json.loads(safe_read(path / conf.schema_path))

            self.validate_lineage_equal(
                test_name=f"{ pathlib.Path(conf.path) / conf.input_path} -> {pathlib.Path(conf.path) /conf.output_path}",
                sql=input_str,
                dialect=conf.dialect,
                schema=schema,
                output_str=output_str,
            )


if __name__ == "__main__":
    unittest.main()
