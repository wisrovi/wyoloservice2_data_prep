"""Declarative WPipe pipeline assembly for dataset preparation and validation."""

from wpipe import Pipeline
from states.validate_dataset_step import validate_dataset_step


def build_data_prep_pipeline(
    tracking_db: str = "/tmp/data_prep.db",
) -> Pipeline:
    """Instantiate and configure dataset preparation pipeline.

    Args:
        tracking_db (str): Path to SQLite tracking database.

    Returns:
        Pipeline: Fully configured WPipe pipeline instance.
    """
    pipe = Pipeline(
        pipeline_name="data_prep_pipe",
        verbose=False,
        tracking_db=tracking_db,
    )
    pipe.set_steps([validate_dataset_step])
    return pipe


# Declarative pipeline singleton for WPipe architecture compliance and visualizer discovery
data_prep_pipeline: Pipeline = build_data_prep_pipeline()

__all__ = ["build_data_prep_pipeline", "data_prep_pipeline"]
