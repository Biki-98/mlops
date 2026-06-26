import os
import sys
from ensure import ensure_annotations
import yaml
import dill
import json
from typing import Any
from pathlib import Path
from mlops.logger import logging
from mlops.exception import CustomException
from box import ConfigBox 
from box.exceptions import BoxValueError
from mlops.constants import CONFIG_FILE_PATH


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox :
    """reads yaml file and returns configbox object

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """

    try:
        with open(path_to_yaml, encoding="utf-8") as f:
            content = yaml.safe_load(f)
            logging.info(f"yaml file: {path_to_yaml} loaded sucessfully.")
            return ConfigBox(content)

    except BoxValueError:
        raise ValueError("yaml file is empty")
    
    except Exception as e:
        raise CustomException(e,sys)
    
@ensure_annotations
def create_dir(path_to_dir: list):
    try:
        for path in path_to_dir:
            os.makedirs(path, exist_ok=True)
            logging.info(f"created directory at {path}")

    except Exception as e:
        raise CustomException(e,sys)
    
# @ensure_annotations
# def save_object(file_path: Path, obj: Optional[Any] = None):
#     try:
#         config = read_yaml(path_to_yaml=CONFIG_FILE_PATH)
#         # checking of artifacts dir
#         root_dir = create_dir([config.artifacts_root])

#         # dir_path = os.path.join("artifacts")
#         # dir_path = os.path.dirname(file_path)
#         # os.makedirs(dir_path, exist_ok=True)

#         # Creating the file_path dir
#         create_dir([file_path])

#         with open(file_path,"wb") as file_obj:
#             dill.dump(obj, file_obj)
    
#     except Exception as e:
#         raise CustomException(e,sys)
# @ensure_annotations
# def save_object(file_path: Path, obj: object)-> None:
#     try:
#         # 1. Isolate the directory path from the file name
#         # If file_path is "artifacts/data_transformation/preprocessor.pkl"
#         # dir_path becomes "artifacts/data_transformation"
#         dir_path = os.path.dirname(file_path)
        
#         # 2. Create the directory (and any parent directories) if they don't exist
#         os.makedirs(dir_path, exist_ok=True)
        
#         # 3. Open the file path in write-binary ("wb") mode and dump the object
#         with open(file_path, "wb") as file_obj:
#             dill.dump(obj, file_obj)
            
#     except Exception as e:
#         raise CustomException(e, sys)

def save_object(file_path: Path, obj: object) -> None:
    try:
        # 1. Use pathlib's native .parent to get the directory
        dir_path = file_path.parent
        
        # 2. Use pathlib's native mkdir to create the directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # 3. Open and dump
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:
        raise CustomException(e, sys)
    
def save_json(data: Any, file_path: str, indent: int = 4) -> None:
    """
    Save a Python object as a JSON file.

    Args:
        data: Any JSON-serializable Python object
        file_path: Full file path (e.g., artifacts/metrics.json)
        indent: JSON indentation level

    Returns:
        str: Path of the saved JSON file/ None
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)

        # return file_path

    except Exception as e:
        raise CustomException(e, sys)