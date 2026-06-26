import pytest
from pathlib import Path
from mlops.config.configuration import ConfigurationManager

@pytest.fixture
def config_manager(tmp_path):
    """Approach is to create a temp config.yaml file inside tmp_path fixture to mimic the behavior for testing."""
    
    # DATA INGESTION
    # creating the config.yaml file structure 
    artifacts_root = tmp_path/ "artifacts"
    ingestion_dir = artifacts_root/ "data_ingestion"
    raw_data_file = ingestion_dir/ "raw.csv"
    train_data_file = ingestion_dir/ "train.csv"
    test_data_file = ingestion_dir/ "test.csv"

    # ensure ingestion dir exist
    ingestion_dir.mkdir(parents=True, exist_ok=True)
    
    # creating a directory for raw data
    raw_data_path = tmp_path/"data"/"data.csv"
    raw_data_path.parent.mkdir(parents=True, exist_ok=True)
    raw_data_path.write_text(
    "gender,race_ethnicity,parental_level_of_education,lunch,"
    "test_preparation_course,math_score,reading_score,writing_score\n"
    "male,group C,bachelor's degree,standard,completed,53,66,73\n"
    "female,group B,some college,free/reduced,completed,68,70,65\n"
    "male,group C,master's degree,standard,none,85,88,82\n"
    "female,group A,associate's degree,free/reduced,none,60,62,58\n"
    "male,group D,high school,standard,completed,78,76,80\n"
    "female,group B,some high school,free/reduced,none,55,58,52\n"
    "male,group E,bachelor's degree,standard,completed,90,92,88\n"
    "female,group C,master's degree,standard,none,82,84,79\n"
    "male,group A,some college,free/reduced,completed,66,68,63\n"
    "female,group D,associate's degree,standard,none,74,72,71\n"
    "male,group B,high school,free/reduced,none,58,56,54\n"
    "female,group E,bachelor's degree,standard,completed,88,90,85\n"
    "male,group C,some high school,free/reduced,none,62,60,59\n"
    "female,group A,master's degree,standard,completed,92,94,89\n"
    "male,group D,some college,standard,none,76,78,73\n"
    "female,group B,associate's degree,free/reduced,completed,64,66,61\n"
    "male,group E,high school,standard,none,80,82,77\n"
    "female,group C,bachelor's degree,free/reduced,none,70,68,67\n"
    "male,group A,some high school,standard,completed,84,86,81\n"
    "female,group D,master's degree,standard,none,86,88,83\n"
    )

    # DATA TRANSFORMATION
    transformation_dir = artifacts_root/ "data_transformation"
    preprocessor_obj_path = transformation_dir/ "preprocessor.pkl"
    transformed_train_data = transformation_dir/ "train.npy"
    transformed_test_data = transformation_dir/ "test.npy"

    # ensure transformation dir exists
    transformation_dir.mkdir(parents=True, exist_ok=True)
    
    # Dummy .pkl — valid enough to prove the file exists and is non-empty.
    # preprocessor_obj_path.write_bytes(b"pkl-stub")

    # MODEL TRAINING
    training_dir = artifacts_root/ "training"
    trained_model_path = training_dir/ "model.dill"
    model_report =  training_dir/ "model_report.json"



    # create temporary yaml file
    config_file = tmp_path/"config.yaml"
    config_file.write_text(f"""
    artifacts_root: {artifacts_root.as_posix()}
    
    data_ingestion:
      raw_data_path: {raw_data_path.as_posix()}
      ingestion_dir: {ingestion_dir.as_posix()}
      raw_data_file: {raw_data_file.as_posix()}
      train_data_file: {train_data_file.as_posix()}
      test_data_file: {test_data_file.as_posix()}
    
    data_transformation:
      root_dir: {transformation_dir.as_posix()}
      preprocessor_obj_path: {preprocessor_obj_path.as_posix()}
      transformed_train_data: {transformed_train_data.as_posix()}
      transformed_test_data: {transformed_test_data.as_posix()}

    training:
      root_dir: artifacts/training
      trained_model_path: artifacts/training/model.dill
      model_report: artifacts/training/model_report.json
    """)

    return ConfigurationManager(config_filepath=config_file)

@pytest.fixture
def data_ingestion_config(config_manager):
    return config_manager.get_data_ingestion_config()

@pytest.fixture
def data_transformation_config(config_manager):
    return config_manager.get_data_transformation_config()

@pytest.fixture
def model_training_config(config_manager):
    return config_manager.get_training_config()





