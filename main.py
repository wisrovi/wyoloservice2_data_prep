"""WYOLO Service 2 Data Prep CLI and execution entrypoint."""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

# Ensure src and root are in sys.path
CURRENT_DIR = str(Path(__file__).resolve().parent)
SRC_DIR = str(Path(__file__).resolve().parent / "src")
for p in [CURRENT_DIR, SRC_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from pipelines import data_prep_pipeline

VERSION = "1.1.0"


def parse_arguments() -> argparse.Namespace:
    """Parse CLI input arguments for dataset preparation pipeline.

    Returns:
        argparse.Namespace: Parsed CLI options.
    """
    parser = argparse.ArgumentParser(description="WYOLO Service 2 Data Prep")
    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help="Path to dataset YAML or classification directory",
    )
    parser.add_argument(
        "--task",
        type=str,
        default="detect",
        choices=["detect", "segment", "classify"],
        help="Vision task domain",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"wyoloservice2_data_prep {VERSION}",
    )
    return parser.parse_args()


def run_pipeline(dataset_path: str, task: str = "detect") -> Dict[str, Any]:
    """Execute dataset preparation and validation pipeline.

    Args:
        dataset_path (str): Filesystem path to dataset.
        task (str): Vision task string.

    Returns:
        Dict[str, Any]: Execution state dictionary.
    """
    payload = {"dataset_path": dataset_path, "task_type": task}
    return data_prep_pipeline.run(payload)


def main() -> None:
    """Entrypoint function handling argument dispatch."""
    args = parse_arguments()
    if args.dataset:
        res = run_pipeline(args.dataset, args.task)
        print(f"Validation Result: {res}")
    else:
        print(f"WYOLO Service 2 Data Prep ({VERSION}) Ready.")


if __name__ == "__main__":
    main()
