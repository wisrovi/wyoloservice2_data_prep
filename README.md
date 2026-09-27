<p align="center">
  <a href="https://linkedin.com/in/wisrovi-rodriguez"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://wisrovi.dev"><img src="https://img.shields.io/badge/Author-wisrovi.dev-111827?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Portal" /></a>
  <a href="https://orcid.org/0009-0005-0710-1861"><img src="https://img.shields.io/badge/ORCID-0009--0005--0710--1861-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License" /></a>
</p>

# 🛠️ NeuralForgeAI Data Prep (`wyoloservice-data-prep`)

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://github.com/wisrovi/wyoloservice2_data_prep)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/wyoloservice-data-prep.svg)](https://pypi.org/project/wyoloservice-data-prep/)

A robust, enterprise-grade **CLI utility and Python library** dedicated to validating YOLO datasets and dispatching real-time notifications across the NeuralForgeAI ecosystem. Built by William Rodriguez (Wisrovi), this library acts as the foundational data gatekeeper before massive GPU compute resources are allocated for hyperparameter sweeps.

---

## 📖 Table of Contents
1. [Introduction](#introduction)
2. [Why Data Validation Matters](#why-data-validation-matters)
3. [Core Features](#core-features)
4. [Installation Guide](#installation-guide)
5. [CLI Usage & Examples](#cli-usage--examples)
6. [Python API Usage](#python-api-usage)
7. [Integration with CI/CD & Celery](#integration-with-cicd--celery)
8. [Slack Notifications](#slack-notifications)
9. [Data Augmentation Roadmap](#data-augmentation-roadmap)
10. [Troubleshooting](#troubleshooting)
11. [About the Author](#about-the-author)

---

## 🌟 Introduction

Training state-of-the-art computer vision models—whether for bounding box detection, semantic segmentation, or image classification—requires strictly formatted datasets. A missing `val` folder, an unmapped class in a `.yaml` file, or corrupted image streams can crash a distributed Optuna training sweep hours after it begins, wasting valuable GPU hours and engineering time.

The `wyoloservice-data-prep` library solves this by providing a lightweight, headless package that can be deployed anywhere—on raw Linux servers, inside Jenkins pipelines, or baked into Docker images. It validates datasets strictly according to Ultralytics YOLOv8 standards.

---

## 🎯 Why Data Validation Matters

In an automated MLOps environment (like NeuralForgeAI), training jobs are queued asynchronously. Without pre-validation:
- Jobs fail silently in remote celery workers.
- Logs are polluted with tracebacks from missing files.
- Teams lose track of which datasets are actually production-ready.

By using this tool, you enforce a strict "Shift-Left" data quality check. Datasets that pass validation immediately trigger a Slack notification to your team, signaling that they are clean and queued for NeuralForge.

---

## ✨ Core Features

1. **Deep YOLO Architecture Validation:**
   - **Classification:** Scans directories to ensure explicit `train/` and `val/` subdirectories exist. Dynamically maps subdirectory names to class labels.
   - **Detection & Segmentation:** Parses `dataset.yaml` files. Validates that `train`, `val`, `nc` (number of classes), and `names` fields exist. Verifies that the internal absolute/relative paths point to valid filesystem targets.
2. **Headless & CI/CD Ready:**
   Designed to run without interactive prompts, making it perfect for GitHub Actions, GitLab CI, Jenkins, or cron jobs.
3. **Slack Integrations:**
   Provides native, robust hooks to notify engineering teams across Slack channels. Custom payloads can alert managers of class imbalances or dataset readiness.
4. **Extensible Augmentation Hooks:**
   Includes structured stubs for balancing datasets dynamically using `albumentations` and `opencv-python-headless` before the actual YOLO engine touches them.

---

## ⚙️ Installation Guide

The library is published on PyPI. It requires Python 3.10 or higher.

### From PyPI (Recommended)
```bash
pip install wyoloservice-data-prep
```

### From Source (Development)
```bash
git clone https://github.com/wisrovi/wyoloservice2_data_prep.git
cd wyoloservice2_data_prep
pip install -e .
```

Installing the package automatically registers the global CLI command `wyolo-validate`.

---

## 🚀 CLI Usage & Examples

The easiest way to use the library is through its built-in Command Line Interface. 

### Validating a Detection Dataset
If you have a standard YOLO detection dataset defined by a `data.yaml` file:

```bash
wyolo-validate --yaml /mnt/samba/datasets/arepo/cicatrices/data.yaml
```

**Expected Output:**
```json
{
  "valid": true,
  "task": "detect",
  "classes": 3,
  "names": ["scratch", "dent", "rust"],
  "train_path": "/mnt/samba/datasets/arepo/cicatrices/images/train"
}
```

### Validating a Classification Dataset
For classification, YOLO expects a raw directory structure (without a yaml). Pass the root directory to the tool:

```bash
wyolo-validate --yaml /datasets/AIDIAGNOST/classification/ages_classification/
```

**Expected Output:**
```json
{
  "valid": true,
  "task": "classify",
  "classes": 4,
  "names": ["ANCIANO", "ADULTO", "JOVEN", "NINO"],
  "train_path": "/datasets/AIDIAGNOST/classification/ages_classification/train"
}
```

---

## 💻 Python API Usage

You can also import the logic directly into your own Python microservices or FastAPI endpoints.

```python
from wyolo_data_prep.validator import check_yolo_dataset

# Validate detection
result_det = check_yolo_dataset("/path/to/detection/dataset.yaml", task_type="detect")
if result_det["valid"]:
    print(f"Dataset is ready! Classes found: {result_det['names']}")
else:
    print(f"Validation failed: {result_det['error']}")

# Validate classification
result_cls = check_yolo_dataset("/path/to/classification/dir", task_type="classify")
if result_cls["valid"]:
    print(f"Found {result_cls['classes']} classes for classification.")
```

---

## 🔗 Integration with CI/CD & Celery

### Within NeuralForge Celery Workers
This library is designed to be bundled inside your `wisrovi/train_service` worker images. Before the Celery task executes `yolo train ...`, it should call the python API to verify the mounted CIFS dataset isn't corrupted.

### Notification Triggers
Combine validation with the Slack notifier to build a complete pipeline:

```python
from wyolo_data_prep.validator import check_yolo_dataset
from wyolo_data_prep.notifier import send_slack_alert

dataset_path = "/path/to/dataset.yaml"
result = check_yolo_dataset(dataset_path)

if result["valid"]:
    send_slack_alert(f"✅ Dataset {dataset_path} passed validation and is ready for training. Classes: {result['classes']}")
else:
    send_slack_alert(f"❌ CRITICAL: Dataset validation failed for {dataset_path}. Error: {result['error']}")
```

---

## 📝 License
This project is open-sourced under the MIT License.

---
**Author:** William Rodriguez (Wisrovi)
*AI Leader & Solutions Architect*
## Licensing and Usage

This project uses a **PolyForm Noncommercial License** model:
- **Community/Research**: Licensed under the PolyForm Noncommercial. See [LICENSE](LICENSE).
- **Commercial**: Requires a commercial license. See [COMMERCIAL.md](COMMERCIAL.md) for details.

### Academic Research
If you use this project in academic research, you are required to cite this repository using the provided `CITATION.cff` and notify the author with a link to your publication.


## Changelog
- Bumped version due to License update to PolyForm Noncommercial and Dual Licensing model.

---

## 👤 Autor & Afiliación Oficial

* **William Steve Rodriguez Villamizar (Wisrovi)**
* **Cargo:** Principal AI Engineer & Applied AI Solutions Architect | Scientific Researcher
* 📧 **Email:** [wisrovi.rodriguez@gmail.com](mailto:wisrovi.rodriguez@gmail.com) / [wisrovi@wisrovi.dev](mailto:wisrovi@wisrovi.dev)
* 🌐 **Portal Oficial:** [wisrovi.dev](https://wisrovi.dev)
* 💼 **LinkedIn:** [wisrovi-rodriguez](https://www.linkedin.com/in/wisrovi-rodriguez/)
* 🆔 **ORCID:** [0009-0005-0710-1861](https://orcid.org/0009-0005-0710-1861)
* 📦 **PyPI:** [pypi.org/user/wisrovi/](https://pypi.org/user/wisrovi/)
* 🐙 **GitHub:** [@wisrovi](https://github.com/wisrovi)
