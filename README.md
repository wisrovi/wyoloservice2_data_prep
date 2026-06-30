# 🛠️ NeuralForgeAI Data Prep (`wyoloservice-data-prep`)

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/wisrovi/wyoloservice2_data_prep)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

A robust CLI utility and Python library for validating YOLO datasets and sending real-time Slack notifications across the NeuralForgeAI ecosystem.

## 🌟 Features

- **Deep YOLO Validation:** Scans local directories or `dataset.yaml` files to verify the existence of `train`/`val` subsets, ensuring compatibility with NeuralForgeAI tasks (`classify`, `detect`, `segment`).
- **Class Extraction:** Automatically parses subdirectories or YAML parameters to count and map dataset classes.
- **Slack Integrations:** Provides native hooks to notify engineering teams when a dataset passes validation and is ready for model training.
- **Data Augmentation Hooks:** Prepared stubs for `albumentations` and `opencv` to auto-balance and augment datasets before training.

## ⚙️ Installation

```bash
git clone https://github.com/wisrovi/wyoloservice2_data_prep.git
cd wyoloservice2_data_prep
pip install -e .
```

This installs the library and registers the `wyolo-validate` command globally.

## 🚀 Usage

You can use the CLI tool directly to validate any YOLO dataset file:

```bash
wyolo-validate --yaml /datasets/AIDIAGNOST/classification/ages_classification/
```

### Inside NeuralForge Containers
This tool is natively designed to be embedded within your Celery worker pipelines or CI/CD actions. It ensures data integrity *before* launching expensive Optuna hyperparameter sweeps.

---
**Author:** William Rodriguez (Wisrovi)