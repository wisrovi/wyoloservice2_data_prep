"""Unit tests for YOLO dataset validator and Slack notifier."""

import os
from unittest.mock import MagicMock, patch
import pytest

from wyolo_data_prep.validator import check_yolo_dataset
from wyolo_data_prep.notifier import SlackNotifier
from dto.dataset_dto import DatasetValidationInput
from states.validate_dataset_step import validate_dataset_step


def test_validator_nonexistent_path() -> None:
    """Validate that checking a nonexistent file path returns valid: False."""
    res = check_yolo_dataset("/nonexistent/path/data.yaml", task_type="detect")
    assert res["valid"] is False
    assert "not found" in res["error"].lower()


def test_validator_classification_directory(tmp_path: pytest.TempPathFactory) -> None:
    """Validate valid classification dataset structure with train/val class folders."""
    dataset_dir = tmp_path / "cls_dataset"
    (dataset_dir / "train" / "cat").mkdir(parents=True)
    (dataset_dir / "train" / "dog").mkdir(parents=True)
    (dataset_dir / "val" / "cat").mkdir(parents=True)
    (dataset_dir / "val" / "dog").mkdir(parents=True)

    res = check_yolo_dataset(str(dataset_dir), task_type="classify")
    assert res["valid"] is True
    assert res["task"] == "classify"
    assert res["classes"] == 2
    assert set(res["names"]) == {"cat", "dog"}


def test_validator_detection_yaml(tmp_path: pytest.TempPathFactory) -> None:
    """Validate valid detection dataset YAML specification."""
    dataset_dir = tmp_path / "det_dataset"
    dataset_dir.mkdir(parents=True)
    train_dir = dataset_dir / "images" / "train"
    train_dir.mkdir(parents=True)

    yaml_file = dataset_dir / "data.yaml"
    yaml_file.write_text(
        "train: images/train\nval: images/train\nnc: 1\nnames: ['car']\n",
        encoding="utf-8",
    )

    res = check_yolo_dataset(str(yaml_file), task_type="detect")
    assert res["valid"] is True
    assert res["classes"] == 1
    assert res["names"] == ["car"]


def test_step_execution() -> None:
    """Validate execution of validate_dataset_step using DTO container."""
    input_dto = DatasetValidationInput(
        dataset_path="/tmp/nonexistent.yaml",
        task_type="detect",
    )
    result = validate_dataset_step(input_dto)
    assert "dataset_validation" in result
    assert result["dataset_validation"]["valid"] is False


def test_slack_notifier_missing_webhook() -> None:
    """Validate that SlackNotifier returns False when no webhook URL is configured."""
    with patch.dict(os.environ, {}, clear=True):
        notifier = SlackNotifier(webhook_url=None)
        assert notifier.send_alert("Title", "Message") is False
