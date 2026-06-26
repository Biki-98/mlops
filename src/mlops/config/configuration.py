from mlops.constants import CONFIG_FILE_PATH
from mlops.utils.common import read_yaml, create_dir
from mlops.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    TrainingConfig,
    PredictionConfig)

from pathlib import Path

# Configuration
class ConfigurationManager:
    def __init__(self, config_filepath = CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        create_dir([self.config.artifacts_root])    # artifacts dir is created

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_dir([config.ingestion_dir])           # artifacts/data_ingestion is created

        data_ingestion_config = DataIngestionConfig(
                                raw_data_path=Path(config.raw_data_path),
                                ingestion_dir=Path(config.ingestion_dir),
                                raw_data_file=Path(config.raw_data_file),
                                train_data_file=Path(config.train_data_file),
                                test_data_file=Path(config.test_data_file)
                                )
        
        return data_ingestion_config
        
    def get_data_transformation_config(self) -> DataTransformationConfig:
        data_transformation = self.config.data_transformation
        train_data_file = self.config.data_ingestion.train_data_file
        test_data_file = self.config.data_ingestion.test_data_file
        create_dir([data_transformation.root_dir]) # artifacts/data_transformation is created

        data_transformation_config = DataTransformationConfig(
            train_data_file=train_data_file,
            test_data_file=test_data_file,
            root_dir=data_transformation.root_dir,
            preprocessor_obj_path=Path(data_transformation.preprocessor_obj_path),
            transformed_train_data=Path(data_transformation.transformed_train_data),
            transformed_test_data=Path(data_transformation.transformed_test_data)
        )

        return data_transformation_config
    
    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        train_data_file = self.config.data_transformation.transformed_train_data
        create_dir([training.root_dir])

        training_config = TrainingConfig(
            root_dir = training.root_dir,
            train_data_file = Path(train_data_file),
            tranied_model_path = Path(training.trained_model_path),
            model_report=Path(training.model_report)
        )

        return training_config
    
    def get_prediction_config(self) -> PredictionConfig:
        return PredictionConfig(
            preprocessor_path=Path(self.config.data_transformation.preprocessor_obj_path),
            model_path=Path(self.config.training.trained_model_path)
        )



        
