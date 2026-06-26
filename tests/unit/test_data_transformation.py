import pytest
import dill
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer

from mlops.components.data_transformation import DataTransformation


def _write_custom_train_test_files(config):
    train_df = pd.DataFrame(
        {
            "gender": ["male", "female", "female"],
            "race_ethnicity": ["group A", "group B", "group C"],
            "parental_level_of_education": [
                "high school",
                "bachelor's degree",
                "some college",
            ],
            "lunch": ["standard", "free/reduced", "standard"],
            "test_preparation_course": ["none", "completed", "none"],
            "reading_score": [70, 80, 90],
            "writing_score": [65, 75, 85],
            "math_score": [60, 72, 88],
        }
    )

    test_df = pd.DataFrame(
        {
            "gender": ["male", "female"],
            "race_ethnicity": ["group B", "group C"],
            "parental_level_of_education": [
                "master's degree",
                "associate's degree",
            ],
            "lunch": ["standard", "free/reduced"],
            "test_preparation_course": ["completed", "none"],
            "reading_score": [78, 68],
            "writing_score": [74, 66],
            "math_score": [76, 64],
        }
    )

    train_path = Path(config.train_data_file)
    # print(train_path)
    test_path = Path(config.test_data_file)
    # print()
    # print(test_path)

    train_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.parent.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(train_path, index=False)
    # print(train_path)
    test_df.to_csv(test_path, index=False)
    # print()
    # print(test_path)

# def test_debug_paths(data_transformation_config):
#     _write_custom_train_test_files(data_transformation_config)


@pytest.fixture
def prepared_data_transformation_config(data_transformation_config):
    """A DataTransformation instance with train/test CSVs already on disk."""
    _write_custom_train_test_files(data_transformation_config)
    return data_transformation_config

def test_get_data_transformer_object_returns_column_transformer(prepared_data_transformation_config):
    transformation = DataTransformation(config=prepared_data_transformation_config)

    preprocessor = transformation.get_data_transformer_object()

    assert isinstance(preprocessor, ColumnTransformer)
    assert len(preprocessor.transformers) == 2


def test_initiate_data_transformation_creates_output_files(prepared_data_transformation_config):
    transformation = DataTransformation(config=prepared_data_transformation_config)
    transformation.initiate_data_transformation()
    
    assert Path(prepared_data_transformation_config.preprocessor_obj_path).exists()
    assert prepared_data_transformation_config.preprocessor_obj_path.stat().st_size > 0
    assert Path(prepared_data_transformation_config.transformed_train_data).exists()
    assert prepared_data_transformation_config.transformed_train_data.stat().st_size > 0
    assert Path(prepared_data_transformation_config.transformed_test_data).exists()
    assert prepared_data_transformation_config.transformed_test_data.stat().st_size > 0


def test_preprocessor_object_is_usable(prepared_data_transformation_config):
    transformation = DataTransformation(config=prepared_data_transformation_config)
    transformation.initiate_data_transformation()

    preprocessor_path = prepared_data_transformation_config.preprocessor_obj_path

    with open(preprocessor_path, "rb") as file:
        preprocessor = dill.load(file)

    assert hasattr(preprocessor, "fit")
    assert hasattr(preprocessor, "transform")

def test_initiate_data_transformation_saves_numpy_arrays(preapared_data_transformation_config):
    transformation = DataTransformation(config=preapared_data_transformation_config)

    transformation.initiate_data_transformation()
    train_array = np.load(preapared_data_transformation_config.transformed_train_data)
    test_array = np.load(preapared_data_transformation_config.transformed_test_data)

    assert train_array.shape[0] == 3
    assert test_array.shape[0] == 2
