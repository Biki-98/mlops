import os
import sys
from mlops.exception import CustomException
from mlops.logger import logging
from dataclasses import dataclass
import shutil
from pathlib import Path
from mlops.config.configuration import DataIngestionConfig
import pandas as pd
from sklearn.model_selection import train_test_split



# components/data_ingestion.py
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def get_dataset(self) -> Path:
        """Fetch dataset from raw folder and copy to artifacts."""
        try:
            source_path = self.config.raw_data_path
            destination_file = self.config.raw_data_file

            logging.info("----- Data ingestion has started ------")

            shutil.copy(source_path, destination_file)

            logging.info(f"Dataset copied from {source_path} to {destination_file}")

            return destination_file
        
        except Exception as e:
            raise CustomException(e, sys)

    def train_test_split(self) -> tuple[Path, Path]:
        """Create train and test split"""
        try:
            logging.info("Creation of train & test set from raw data started --->")

            df = pd.read_csv(self.config.raw_data_path)
            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

            train_df.to_csv(self.config.train_data_file, index=False)
            test_df.to_csv(self.config.test_data_file, index=False)

            logging.info("Train & test set successfully created")

        except Exception as e:
            raise CustomException(e,sys)
