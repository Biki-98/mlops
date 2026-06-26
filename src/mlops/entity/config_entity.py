from dataclasses import dataclass
from pathlib import Path

# data ingestion
@dataclass(frozen=True)
class DataIngestionConfig:
    raw_data_path: Path
    ingestion_dir: Path
    raw_data_file: Path
    train_data_file: Path
    test_data_file: Path

# data transformation
@dataclass(frozen=True)
class DataTransformationConfig:
    train_data_file: Path
    test_data_file: Path
    root_dir: Path
    preprocessor_obj_path: Path
    transformed_train_data: Path
    transformed_test_data: Path

# model training
@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    train_data_file: Path
    tranied_model_path: Path
    model_report: Path

@dataclass(frozen=True)
class PredictionConfig:
    model_path: Path
    preprocessor_path: Path
    
