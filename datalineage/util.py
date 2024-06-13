from typing import Optional, Any
from pathlib import Path
import os

from datalineage.logger import setup_logger

logger = setup_logger(__name__)


def read_file(file_path: str) -> str:
    with open(file_path, "rt") as file:
        return file.read()


def safe_read(file_path: str) -> Optional[str]:
    try:
        return read_file(file_path)
    except Exception as e:
        logger.error(str(e))
        return None


def write_file(file_path: str, content: str) -> None:
    Path(os.path.dirname(file_path)).mkdir(parents=True, exist_ok=True)

    with open(file_path, "wt") as file:
        file.write(content)


def safe_write(file_path: str, content: str) -> None:
    try:
        write_file(file_path, content)
    except Exception as e:
        logger.error(str(e))


def require_non_null(v: Any, msg: Optional[str] = None) -> Any:
    """value must be not None, otherwise will raise an exception with the optional provided msg."""

    msg = msg or f"Value must be not null, currently {str(v)}"

    if v is None:
        raise ValueError(msg)

    return v
