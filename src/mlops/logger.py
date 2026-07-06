# import logging
# import os
# from datetime import datetime

# # Checking/creating logs folder
# logs_dir = os.path.join(os.getcwd(), "logs")
# os.makedirs(logs_dir, exist_ok=True)

# # Get current timestamp once to ensure consistency
# current_time = datetime.now()

# # Create date folder (only year-month-day, same for entire day)
# date_folder = current_time.strftime("%d_%m_%y")
# date_folder_path = os.path.join(logs_dir, date_folder)
# os.makedirs(date_folder_path, exist_ok=True)

# # Create unique log file per execution (includes time down to seconds)
# LOG_FILE = f"{current_time.strftime('%d_%m_%y_%H_%M_%S')}.log"
# LOG_FILE_PATH = os.path.join(date_folder_path, LOG_FILE)

# # Configure logging with both file and console handlers
# logging.basicConfig(
#     filename=LOG_FILE_PATH,
#     format="[ %(asctime)s ] %(lineno)d %(filename)s %(name)s - %(levelname)s - %(message)s",
#     level=logging.INFO,
#     force=True
# )

# if __name__ == "__main__":
#     logger = logging.getLogger(__name__)
#     logger.info("Logger initialized")

# def setup_logger():
#     # Checking/creating logs folder
#     logs_dir = os.path.join(os.getcwd(), "logs")
#     os.makedirs(logs_dir, exist_ok=True)

#     # Get current timestamp once to ensure consistency
#     current_time = datetime.now()

#     # Create date folder (only year-month-day, same for entire day)
#     date_folder = current_time.strftime("%d_%m_%y")
#     date_folder_path = os.path.join(logs_dir, date_folder)
#     os.makedirs(date_folder_path, exist_ok=True)

#     # Create unique log file per execution (includes time down to seconds)
#     LOG_FILE = f"{current_time.strftime('%d_%m_%y_%H_%M_%S')}.log"
#     LOG_FILE_PATH = os.path.join(date_folder_path, LOG_FILE)

#     # Configure logging with both file and console handlers
#     logging.basicConfig(
#         filename=LOG_FILE_PATH,
#         format="[ %(asctime)s ] %(lineno)d %(filename)s %(name)s - %(levelname)s - %(message)s",
#         level=logging.INFO,
#         force=True
#     )

#     return logging


import logging
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FORMAT = (
    "[ %(asctime)s ] %(lineno)d %(filename)s %(name)s - %(levelname)s - %(message)s"
)


def _build_log_file_path() -> Path:
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    current_time = datetime.now()
    date_folder = logs_dir / current_time.strftime("%d_%m_%y")
    date_folder.mkdir(parents=True, exist_ok=True)

    log_file = f"{current_time.strftime('%d_%m_%y_%H_%M_%S')}.log"
    return date_folder / log_file


def setup_logger(force=False):
    root_logger = logging.getLogger()

    if getattr(root_logger, "_mlops_configured", False) and not force:
        return logging

    log_file_path = _build_log_file_path()

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(log_file_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=force,
    )

    root_logger = logging.getLogger()
    root_logger._mlops_configured = True
    root_logger._mlops_log_file_path = str(log_file_path)

    return logging


logging = setup_logger()
