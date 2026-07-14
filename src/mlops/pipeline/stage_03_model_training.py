import sys
import os
from mlops.logger import logging
from mlops.config.configuration import ConfigurationManager
from mlops.components.model_training import Training
from mlops.exception import CustomException
from mlops.utils.common import get_env


STAGE_NAME = "Model Training"

class ModelTrainingPipeline:
    def __int__(self):
        pass

    def main(self):
        try:
            logging.info(f"{STAGE_NAME} pipeline started ---->")
            config = ConfigurationManager()
            model_training_config = config.get_training_config()
            model_trainer = Training(config=model_training_config)
            model_trainer.train()
            model_trainer.evaluate()
            model_trainer.log_to_mlflow(
            registered_model_name="student-performance-model",
            experiment_name="student-performance-training",
            run_name="linear-regression",
            tracking_uri=get_env("MLFLOW_TRACKING_URI"))
            
            logging.info(f"{STAGE_NAME} pipeline executed successfully")

        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=="__main__":
    try:
        obj = ModelTrainingPipeline()
        obj.main()

    except Exception as e:
        raise CustomException(e,sys)
        