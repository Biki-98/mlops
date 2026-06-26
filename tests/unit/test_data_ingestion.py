import os
from pathlib import Path
from mlops.components.data_ingestion import DataIngestion


def test_data_ingestion_get_file(tmp_path, data_ingestion_config):
    """This function tests the get_dataset method of the DataIngestion class."""
    di = DataIngestion(config=data_ingestion_config)
    returned_path = di.get_dataset()

    # raw_data_file = tmp_path/ "artifacts"/ "data_ingestion"/ "raw.csv"
    
    # assert returned_path == data_ingestion_config.raw_data_file
    # 👉 Focus on behavior, not exact internal path
    assert Path(returned_path).exists()
    assert Path(returned_path).stat().st_size > 0
    # assert os.path.getsize(returned_path) > 0
    # assert Path(returned_path).stat().st_size > 0
    

def test_train_test_split(tmp_path, data_ingestion_config):
    """This function tests the train test split of the dataset."""
    di = DataIngestion(config=data_ingestion_config)
    di.train_test_split()

    assert data_ingestion_config.train_data_file.exists()
    assert data_ingestion_config.test_data_file.exists()
    assert data_ingestion_config.train_data_file.stat().st_size > 0
    assert data_ingestion_config.test_data_file.stat().st_size > 0
    print(data_ingestion_config.train_data_file)
    print(data_ingestion_config.test_data_file)









# current_file = Path(__file__).resolve()

# # .../Tutorial/tests/unit/test_data_ingestion.py -> go up 3 levels to .../Tutorial
# PROJECT_ROOT = current_file.parents[2]  # unit -> tests -> Tutorial
# raw_csv_path = PROJECT_ROOT / "artifacts" / "data_ingestion" / "raw.csv"
# size = raw_csv_path.stat().st_size
# # or
# # size = os.path.getsize(raw_csv_path)
# size_mb = size/ (1024)  
# print(f"raw.csv: {size:,} bytes ({size_mb:.2f} KB)")


