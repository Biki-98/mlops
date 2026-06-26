import sys
from mlops.logger import logging
from mlops.exception import CustomException
from mlops.config.configuration import ConfigurationManager
from mlops.components.data_ingestion import DataIngestion

STAGE_NAME = "Data Ingestion"

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logging.info(f"{STAGE_NAME} Pipeline started ----->")
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.get_dataset()
            data_ingestion.train_test_split()
            logging.info(f"{STAGE_NAME} Pipeline executed successfully.")

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    try:
        obj = DataIngestionPipeline()
        obj.main()
    
    except Exception as e:
        raise CustomException(e,sys)