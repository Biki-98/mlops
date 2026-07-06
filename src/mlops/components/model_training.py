import sys
import os
import mlflow
import mlflow.sklearn
from mlops.entity.config_entity import TrainingConfig
from mlops.exception import CustomException
from  mlops.logger import logging
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from mlops.utils.common import save_json, save_object
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.lr = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_train_pred = None
        self.y_test_pred = None
        self.report = None
        self._is_trained = False

    def train(self):
        """This function is used for model training"""

        try:

            logging.info("Training started --->")
            logging.info("Loading of transformed train data started--->")
            
            train_arr = np.load(self.config.train_data_file)
            
            logging.info("Transformed train data loaded successfully.")
            
            X = train_arr[:,:-1]
            y = train_arr[:,-1]
            
            logging.info("Starting train test split---->")
            
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X,y,test_size=0.2,random_state=42)

            logging.info("Train-test-split is done successfully.")

            self.lr = LinearRegression()

            logging.info("Model fitting started -->")

            self.lr.fit(self.X_train, self.y_train) # Train/fitting the model
            self._is_trained = True

            logging.info("Model fitting completed.")
            logging.info("Predictions are made.")

        except Exception as e:
            raise CustomException(e,sys)

    
    @staticmethod
    def _evaluate_model(true, predicted):
        model_report = {}
        mae = mean_absolute_error(true, predicted)
        mse = mean_squared_error(true, predicted)
        rmse = np.sqrt(mean_squared_error(true, predicted))
        r2_value = r2_score(true, predicted)
        
        model_report = {
            "mae": mae,
            "rmse": rmse,
            "r2_score": r2_value
        }
        return model_report
    
    def evaluate(self):
        """This function is for evaluation"""

        if not self._is_trained:
                raise RuntimeError("You must call train() before evaluate().")


        try:

            # Make predictions
            self.y_train_pred = self.lr.predict(self.X_train)
            self.y_test_pred = self.lr.predict(self.X_test)
            

            # Evaluate Train and Test dataset
            y_train_model_report = self._evaluate_model(self.y_train, self.y_train_pred)
            y_test_model_report = self._evaluate_model(self.y_test, self.y_test_pred)

            save_object(file_path=self.config.tranied_model_path,
                        obj=self.lr)
            
            logging.info(f"Trained model is saved at {self.config.tranied_model_path}")
            
            report = {"train": y_train_model_report,"test": y_test_model_report}
            self.report = report

            save_json(data=report, file_path=self.config.model_report)

            logging.info(f"Model report of train and test set is saved at {self.config.model_report}")
            return report

        except Exception as e:
            raise CustomException(e,sys)

    def log_to_mlflow(
        self,
        registered_model_name=None,
        experiment_name=None,
        run_name=None,
        tracking_uri=os.environ["MLFLOW_TRACKING_URI"],
    ):
        """Log model metrics, report artifact, and model to MLflow."""

        if not self._is_trained:
            raise RuntimeError("You must call train() before log_to_mlflow().")

        if self.report is None:
            self.evaluate()

        try:
            if tracking_uri:
                mlflow.set_tracking_uri(tracking_uri)

            if experiment_name:
                mlflow.set_experiment(experiment_name)

            metrics = {
                "train_mae": self.report["train"]["mae"],
                "train_rmse": self.report["train"]["rmse"],
                "train_r2_score": self.report["train"]["r2_score"],
                "test_mae": self.report["test"]["mae"],
                "test_rmse": self.report["test"]["rmse"],
                "test_r2_score": self.report["test"]["r2_score"],
            }

            with mlflow.start_run(run_name=run_name):
                mlflow.log_metrics(metrics)
                mlflow.log_artifact(str(self.config.model_report))

                model_info = mlflow.sklearn.log_model(
                    sk_model=self.lr,
                    artifact_path="model",
                    registered_model_name=registered_model_name,
                )

            logging.info("Model metrics, report, and model logged to MLflow successfully.")
            return model_info

        except Exception as e:
            raise CustomException(e, sys)


        
