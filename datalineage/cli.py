import click
import json

from datalineage.renderer import Renderer, ensure_renderer

from datalineage.lineage import lineage
from datalineage.util import safe_read, safe_write
from datalineage.logger import setup_logger

logger = setup_logger(__name__)


@click.command()
@click.option("-i", "--input", prompt="Input path", help="The input path of the sql.")
@click.option("-o", "--output", default=None, prompt=False, help="The output path of the result.")
@click.option(
    "-r",
    "--renderer",
    default="mermaid",
    type=click.Choice(["json", "mermaid"], case_sensitive=False),
    help="The renderer used to render format of lineage output to file.",
)
@click.option(
    "-d", "--dialect", default=None, prompt=False, help="The dialect which input belong to."
)
@click.option(
    "--schema-path",
    prompt="Path to schema json file",
    help="Path to schema json file, which contains sqlglot schema.",
)
def make_lineage(input, output, renderer, dialect, schema_path):
    """Generate column level lineage for a query."""

    sql = safe_read(input)
    if not sql:
        raise ValueError("Can not read input sql from file: {}".format(input))

    schema = safe_read(schema_path)
    schema = json.loads(schema) if schema else None

    tree = lineage(sql, dialect, schema)

    out_renderer: Renderer = ensure_renderer(renderer)
    rendered_content = out_renderer.render(tree)

    if output:
        logger.info("Rendering output into a file")
        safe_write(output, rendered_content)
    else:
        logger.info("Rendering output into stdout")
        click.echo(rendered_content)


def main():
    make_lineage()


if __name__ == "__main__":
    main()
