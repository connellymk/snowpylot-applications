import logging
import importlib
import sys
from pathlib import Path
from typing import Any, Union

try:
    from snowpylot import caaml_parser
except ImportError:
    repo_root = Path(__file__).resolve().parents[2]
    local_src = repo_root / "snowpylot" / "src"
    if local_src.is_dir():
        sys.path.insert(0, str(local_src))
        sys.modules.pop("snowpylot", None)
        try:
            caaml_parser = importlib.import_module("snowpylot").caaml_parser
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "snowpylot dependencies are not installed. Install "
                "snowpylot-applications/requirements.txt before running this notebook."
            ) from exc
    else:
        raise

logger = logging.getLogger(__name__)


def parse_caaml_directory(
    directory: Union[str, Path], pattern: str = "*.xml"
) -> list[Any]:
    """
    Parse all CAAML XML files in a directory and return SnowPylot pit objects.

    Files that fail to parse are logged and skipped.
    """
    directory = Path(directory)
    if not directory.is_dir():
        raise FileNotFoundError(f"CAAML directory does not exist: {directory}")

    all_profiles: list[Any] = []
    failed_files: list[tuple[str, str]] = []
    xml_files = sorted(directory.glob(pattern))

    for file_path in xml_files:
        try:
            profile = caaml_parser(str(file_path))
            all_profiles.append(profile)
        except Exception as exc:
            failed_files.append((file_path.name, str(exc)))
            logger.warning("Failed to parse %s: %s", file_path.name, exc)

    logger.info(
        "Successfully parsed %s of %s files (%s failed)",
        len(all_profiles),
        len(xml_files),
        len(failed_files),
    )

    return all_profiles
