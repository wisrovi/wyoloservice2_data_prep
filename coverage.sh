#!/bin/bash
# Calculates test coverage inside a Docker container
echo "Calculating test coverage in Docker container..."
docker run --rm -e PYTHONDONTWRITEBYTECODE=1 -v $(pwd):/app -w /app python:3.10-slim bash -c "pip install pytest pytest-cov pydantic wpipe pyyaml requests && PYTHONPATH=/app/src:/app pytest --cov=src --cov-report=term-missing tests/"
