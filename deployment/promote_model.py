from mlflow import MlflowClient
from mlops.utils.common import get_env
from mlops.logger import logging

client = MlflowClient()
model_name = get_env("MLFLOW_MODEL_NAME") 
# version = "3"
alias = get_env("MLFLOW_MODEL_ALIAS")

try:

    versions = client.search_model_versions(f"name='{model_name}'")
    latest_version = str(max(int(v.version) for v in versions))

    # Check if the version exists first
    mv = client.get_model_version(model_name, latest_version)
    print(f"Found latest version {latest_version}. Current stage: {mv.current_stage}")
    
    # Attempt to set the alias
    client.set_registered_model_alias(model_name, alias, latest_version)
    print(f"Success: Alias '{alias}' set to version {latest_version}.")
    
except Exception as e:
    print(f"Error occurred: {e}")

# deployment/promote_model.py

import sys
import logging
from mlflow import MlflowClient
from mlops.utils.common import get_env

# WHY: structured logging > print
# print has no levels, no timestamps, no machine-parseable format
# In CI/CD, you need to distinguish INFO from ERROR
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
# )
# logger = logging.getLogger("promote_model")


def get_latest_validated_version(client: MlflowClient, model_name: str) -> str:
    """
    WHY THIS EXISTS AS A SEPARATE FUNCTION:
    - Testable in isolation (unit test this without touching MLflow)
    - Single Responsibility Principle: version selection is its own concern
    - Later you can swap 'latest version' for 'best metric version'
    """
    versions = client.search_model_versions(f"name='{model_name}'")

    # WHY: Explicit guard instead of letting max() crash opaquely
    if not versions:
        raise ValueError(
            f"No versions found for model '{model_name}'. "
            "Has the model been registered yet?"
        )

    # NOTE FOR YOU: This is still 'latest by version number'
    # In a mature system, you'd filter by run metrics here:
    # e.g., only consider versions where accuracy > threshold
    latest = str(max(int(v.version) for v in versions))
    return latest


def promote_model(
    client: MlflowClient,
    model_name: str,
    alias: str,
    version: str
) -> None:
    """
    WHY PROMOTION IS SEPARATED FROM GATE-CHECKING:
    Single Responsibility. This function does ONE thing.
    Makes it easier to test, mock, and reason about.
    """
    client.set_registered_model_alias(model_name, alias, version)
    logging.info(
        f"PROMOTED | model='{model_name}' | "
        f"version={version} | alias='{alias}'"
    )
    # WHY LOG IN THIS FORMAT:
    # Pipe-separated key=value is machine-parseable
    # Tools like Datadog, Grafana Loki, CloudWatch can extract
    # these as structured fields automatically


def main():
    model_name = get_env("MLFLOW_MODEL_NAME")
    alias = get_env("MLFLOW_MODEL_ALIAS")

    client = MlflowClient()

    try:
        latest_version = get_latest_validated_version(client, model_name)
        logging.info(f"Candidate version for promotion: {latest_version}")

        gates_passed = check_quality_gates(client, model_name, latest_version)
        if not gates_passed:
            logging.error("Promotion BLOCKED: quality gates not met.")
            sys.exit(1)  # WHY sys.exit(1): CI/CD reads exit codes.
                         # exit(1) = failure → pipeline stops
                         # exit(0) = success → pipeline continues

        promote_model(client, model_name, alias, latest_version)

    except ValueError as e:
        # WHY SEPARATE VALUEERROR FROM GENERIC EXCEPTION:
        # This is a known, expected failure mode (no versions registered)
        # Handle it specifically so your logs are actionable
        logging.error(f"Configuration error: {e}")
        sys.exit(1)

    except Exception as e:
        # Only truly unexpected errors reach here
        logging.exception(f"Unexpected error during promotion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()