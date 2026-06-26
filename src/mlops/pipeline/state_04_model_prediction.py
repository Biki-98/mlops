import sys
import dill
import pandas as pd
from mlops.logger import logging
from mlops.config.configuration import ConfigurationManager
from mlops.exception import CustomException


class PredictPipeline:
    def __init__(self):
        config = ConfigurationManager()
        pred_config = config.get_prediction_config()

        # In case of using pathlib.Path we can write like this,
        
        with pred_config.preprocessor_path.open("rb") as f1:
            self.preprocessor = dill.load(f1)

        with pred_config.model_path.open("rb") as f2:
            self.model = dill.load(f2)

        logging.info("model.dill and preprocessor.pkl objects are loaded successfully.")

    def predict(self, features):
        """This method will do the prediction."""
        try:
            logging.info("Starting prediction data transformation and prediction.")
            
            data_transformed = self.preprocessor.transform(features)
            preds = self.model.predict(data_transformed)

            logging.info("Finished prediction data transformatin and prediction.")

            return preds
        
        except Exception as e:
            raise CustomException(e,sys)
        

class CustomData:
    def __init__(  self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender

        self.race_ethnicity = race_ethnicity

        self.parental_level_of_education = parental_level_of_education

        self.lunch = lunch

        self.test_preparation_course = test_preparation_course

        self.reading_score = reading_score

        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
