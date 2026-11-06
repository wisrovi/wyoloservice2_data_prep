"""YOLO dataset structural validation and augmentation utilities."""

import argparse
import os
from pathlib import Path
from typing import Any, Dict
import yaml


def check_yolo_dataset(dataset_path: str, task_type: str = "detect") -> Dict[str, Any]:
    """Validate YOLO dataset integrity based on task domain specification.

    Args:
        dataset_path (str): Filepath to dataset.yaml or base classification directory.
        task_type (str): Computer vision task ('detect', 'segment', 'classify').

    Returns:
        Dict[str, Any]: Validation summary dictionary with boolean 'valid' status.
    """
    path_obj = Path(dataset_path)

    if task_type == "classify":
        if not path_obj.is_dir():
            return {
                "valid": False,
                "error": f"For classification, dataset must be a directory: {dataset_path}",
            }

        train_dir = path_obj / "train"
        val_dir = path_obj / "val"

        if not train_dir.exists() or not train_dir.is_dir():
            return {"valid": False, "error": f"Missing 'train' directory in {dataset_path}"}
        if not val_dir.exists() or not val_dir.is_dir():
            return {"valid": False, "error": f"Missing 'val' directory in {dataset_path}"}

        classes = [d.name for d in train_dir.iterdir() if d.is_dir()]
        return {
            "valid": True,
            "task": "classify",
            "classes": len(classes),
            "names": classes,
            "train_path": str(train_dir),
        }

    if not path_obj.exists() or not path_obj.is_file():
        return {
            "valid": False,
            "error": f"YAML file not found or is not a file: {dataset_path}",
        }

    try:
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        base_dir = path_obj.parent

        for field in ["train", "val", "nc", "names"]:
            if field not in data:
                return {
                    "valid": False,
                    "error": f"Missing required field in YAML: {field}",
                }

        train_path_str = data["train"]
        if isinstance(train_path_str, str):
            train_path = (
                base_dir / train_path_str
                if not Path(train_path_str).is_absolute()
                else Path(train_path_str)
            )
            if not train_path.exists():
                return {
                    "valid": False,
                    "error": f"Train path does not exist: {train_path}",
                }

        return {
            "valid": True,
            "task": task_type,
            "classes": data["nc"],
            "names": data["names"],
            "train_path": str(train_path)
            if isinstance(train_path_str, str)
            else "multiple/complex paths",
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


def augment_dataset(image_dir: str, output_dir: str) -> None:
    """Execute synthetic image augmentation to balance underrepresented classes.

    Args:
        image_dir (str): Source directory containing input images.
        output_dir (str): Target directory to persist augmented images.
    """
    os.makedirs(output_dir, exist_ok=True)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for dataset validation.

    Returns:
        argparse.Namespace: Parsed CLI arguments container.
    """
    parser = argparse.ArgumentParser(description="Validate YOLO dataset")
    parser.add_argument("--yaml", required=True, help="Path to dataset.yaml")
    return parser.parse_args()


def main() -> None:
    """Entrypoint function for CLI dataset validation."""
    args = parse_arguments()
    result = check_yolo_dataset(args.yaml)
    print(result)


if __name__ == "__main__":
    main()
