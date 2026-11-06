"""WPipe step for validating YOLO dataset configuration and directories."""

import sys
from pathlib import Path
from typing import Any, Dict
from wpipe import step, to_obj

# Ensure src is in sys.path
SRC_DIR = str(Path(__file__).resolve().parent.parent / "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from dto.dataset_dto import DatasetValidationInput
from wyolo_data_prep.validator import check_yolo_dataset


@step(name="validate_dataset_step", version="v1.0", tags=["data_prep", "validation"])
@to_obj(DatasetValidationInput)
def validate_dataset_step(input_data: DatasetValidationInput) -> Dict[str, Any]:
    """Execute YOLO dataset validation as a pipeline step.

    Args:
        input_data (DatasetValidationInput): Input container with dataset path and task.

    Returns:
        Dict[str, Any]: Validation results dictionary.
    """
    result = check_yolo_dataset(
        dataset_path=input_data.dataset_path,
        task_type=input_data.task_type,
    )
    return {"dataset_validation": result}
