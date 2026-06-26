import os
from pathlib import Path
import logging

# logging string
logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")

# list_of_files = [
#     ".github/workflows/.gitkeep",
#     "data/raw",
#     "data/processed",
#     "artifacts/models",
#     "logs/",
#     "notebooks/",              # Research & trials
#     "src/__init__.py",
#     "src/components/__init__.py",
#     "src/utils/__init__.py",
#     "src/config/__init__.py",
#     "src/config/configuration.py",
#     "src/pipeline/__init__.py",
#     "src/orchestration/__init__.py",
#     "monitoring/metrics",       # prometheus
#     "monitoring/dashboards",    # Grafana
#     "monitoring/drift",         # Evidently AI
#     "config/config.yaml",
#     "tests/",
#     "main.py",
#     "app.py",
#     "dvc.yaml",
#     "prefect.yaml",
#     "Dockerfile",
#     "requirements.txt",
#     ".gitignore",
#     "setup.py",
#     "templates/index.html"
# ]

# for filepath in list_of_files:
#     filepath = Path(filepath)
#     file_dir, file_name = os.path.split(filepath)

#     if file_dir !="":
#         os.makedirs(file_dir, exist_ok=True)
#         logging.info(f"creating directory; {file_dir} for the file name {file_name}")

#     if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
#         with open(filepath, "w") as f:
#             pass
#             logging.info(f"creating empty file {filepath}")
    
#     else:
#         logging.info(f"{filepath} is already exists.")

dirs = ["data/raw/",
        "data/processed/",
        "artifacts/models/", 
        "logs/",
        "tests/",
        "notebooks/",
        "monitoring/metrics/",       # prometheus
        "monitoring/dashboards/",    # Grafana
        "monitoring/drift/"          # Evidently AI
        ]

files = [".github/workflows/.gitkeep",
         "src/__init__.py",
         "src/components/__init__.py",
         "src/utils/__init__.py",
         "src/config/__init__.py",
         "src/config/configuration.py",
         "src/pipeline/__init__.py",
         "src/orchestration/__init__.py",
         "config/config.yaml",
         "main.py",
         "app.py",
         "dvc.yaml",
         "prefect.yaml",
         "Dockerfile",
         "requirements.txt",
         ".gitignore",
         "setup.py",
         "templates/index.html"]

# Create directories first
logging.info("=== Creating directories ===")
for dir_path in dirs:
    path = Path(dir_path)
    try:
        path.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.is_dir():
            logging.info(f"✓ Directory created/exists: {path}")
        else:
            logging.warning(f"✗ Directory creation failed: {path}")
    except Exception as e:
        logging.error(f"✗ Failed to create directory {path}: {e}")

# Create files second
logging.info("=== Creating files ===")
for file_path in files:
    path = Path(file_path)
    try:
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        logging.info(f"✓ File created/exists: {path}")
    except Exception as e:
        logging.error(f"✗ Failed to create file {path}: {e}")

logging.info("=== Directory structure setup complete ===")