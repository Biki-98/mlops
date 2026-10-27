from mlflow import MlflowClient
from mlops.utils.common import get_env
from mlops.logger import logging

client = MlflowClient()

model_name = get_env("MLFLOW_MODEL_NAME") 
# version = "3"
alias = get_env("MLFLOW_MODEL_ALIAS")

try:

    versions = client.search_model_versions(f"name='{model_name}'")

    if not versions:
        raise ValueError(
            f"No versions found for model '{model_name}'. "
            "Has the model been registered yet?"
        )
    
    latest_version = str(max(int(v.version) for v in versions))

    # Check if the version exists first
    mv = client.get_model_version(model_name, latest_version)
    logging.info(f"Found latest version {latest_version}. Current stage: {mv.current_stage}")
    
    # Attempt to set the alias
    client.set_registered_model_alias(model_name, alias, latest_version)
    logging.info(f"Success: Alias '{alias}' set to version {latest_version}.")
    
except Exception as e:
    print(f"Error occurred: {e}")
