"""Data Transfer Objects (DTO) for dataset preparation and validation."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class DatasetValidationInput(BaseModel):
    """Input payload providing dataset path and optional task specification.

    Attributes:
        dataset_path: Path to dataset YAML configuration or directory.
        task_type: Vision task ('detect', 'segment', 'classify').
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    dataset_path: str = Field(..., description="Path to dataset YAML or folder")
    task_type: str = Field(default="detect", description="Vision task domain")


class DatasetValidationResult(BaseModel):
    """Output container capturing verification outcomes and class statistics.

    Attributes:
        valid: True if dataset conforms to requirements, False otherwise.
        task: Detected or evaluated vision task.
        classes: Number of distinct classes or categories.
        names: List or dictionary of class labels.
        train_path: Resolved path to training partition.
        error: Optional failure diagnosis message.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    valid: bool = Field(..., description="Validation success indicator")
    task: Optional[str] = Field(default=None, description="Task domain")
    classes: Optional[int] = Field(default=None, description="Total class count")
    names: Optional[Any] = Field(default=None, description="Class label names")
    train_path: Optional[str] = Field(default=None, description="Path to training images")
    error: Optional[str] = Field(default=None, description="Error diagnostics if invalid")
