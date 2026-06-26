import sys
from mlops.config.configuration import ConfigurationManager
from mlops.logger import logging
from mlops.exception import CustomException
from mlops.components.data_transformation import DataTransformation

STAGE_NAME ="Data Transformation"

class DataTransformationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logging.info(f"{STAGE_NAME} pipeline started ---->")
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            data_transformation.initiate_data_transformation()
            logging.info(f"{STAGE_NAME} Pipeline executed successfully.")
        
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    try:
        obj = DataTransformationPipeline()
        obj.main()
    
    except Exception as e:
        raise CustomException(e,sys)