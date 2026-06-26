import sys
from mlops.logger import logging
from mlops.exception import CustomException
from mlops.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from mlops.pipeline.stage_02_data_transformation import DataTransformationPipeline
from mlops.pipeline.stage_03_model_training import ModelTrainingPipeline

# DATA INGESTION

try:
    data_ingeston = DataIngestionPipeline()
    data_ingeston.main()

except Exception as e:
    raise CustomException(e,sys)

# DATA TRANSFORMATION

try:
    data_transformation = DataTransformationPipeline()
    data_transformation.main()

except Exception as e:
    raise CustomException(e,sys)

# MODEL TRAINING

try:
    model_training = ModelTrainingPipeline()
    model_training.main()

except Exception as e:
    raise CustomException(e,sys)