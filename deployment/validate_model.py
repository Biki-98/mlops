import sys
from mlflow import MlflowClient
from mlflow.exceptions import RestException, MlflowException
from mlops.utils.common import get_env
from mlops.logger import logging
from mlops.exception import CustomException

model_name = get_env("MLFLOW_MODEL_NAME") 
alias = get_env("MLFLOW_MODEL_ALIAS")

def get_champion_r2(client: MlflowClient, model_name: str) -> float | None:
    """
    Fetch the r2_score of the current champion model (Production stage).
    Returns None if no champion exists yet (first deployment scenario).
    """
    try:
        champ_version_info = client.get_model_version_by_alias(name=model_name, alias=alias)

        if not champ_version_info:
            logging.info(
                "No champion model is found in Production stage. "
                "This is likely the first deployment."
            )
            return None

        champion_version = champ_version_info.version
        champion_run_id = champ_version_info.run_id
        run = client.get_run(champ_version_info.run_id)
        champion_r2_score = run.data.metrics.get("test_r2_score", None)

        return champion_r2_score


    except Exception as e:
        raise CustomException(e, sys)


def check_quality_gates(client: MlflowClient, model_name: str, version: str) -> bool:
    """
    Quality gates for challenger model promotion.

    Gate 1 — Minimum r2 threshold:
        Challenger must meet the absolute minimum quality bar.

    Gate 2 — Champion comparison:
        Challenger must be strictly better than the current
        production champion. Skipped if no champion exists yet.
    """
     # --- Fetch Challenger Metrics ---
    mv = client.get_model_version(model_name, version)
    # run_id = mv.run_id
    run = client.get_run(mv.run_id)
    challenger_r2_score = run.data.metrics.get("test_r2_score", None)

    MIN_R2_THRESHOLD = float(get_env("MIN_R2_THRESHOLD", default="0.75"))

    logging.info(
        f"Challenger model: version={version}, "
        f"r2_score={challenger_r2_score}, "
        f"minimum_threshold={MIN_R2_THRESHOLD}"
    )

    # --- Gate 1: Challenger must have r2 logged ---
    if challenger_r2_score is None:
        logging.warning(
            f"Gate 1 FAILED: No test_r2_score metric logged for challenger model."
        )
        return False

    # --- Gate 2: Challenger must meet minimum r2 score threshold ---
    if challenger_r2_score < MIN_R2_THRESHOLD:
        logging.warning(
            f"Gate 2 FAILED: Challenger r2 score = {challenger_r2_score:.4f} "
            f"is below minimum threshold = {MIN_R2_THRESHOLD:.4f}."
        ) 
        return False

    logging.info(
        f"Gate 2 PASSED: Challenger r2 = {challenger_r2_score:.4f} "
        f">= threshold={MIN_R2_THRESHOLD:.4f}."
    )

    # --- Gate 3: Challenger must beat champion ---
    champion_r2_score = get_champion_r2(client=client, model_name=model_name)

    if champion_r2_score is None:
        # First deployment — no champion exists yet
        # Minimum threshold already passed — safe to promote
        logging.info(
            "Gate 3 SKIPPED: No champion exists. "
            "Challenger will become the first production model."
        )

    else:
        if challenger_r2_score <= champion_r2_score:
            logging.warning(
                f"Gate 3 FAILED: Challenger r2={challenger_r2_score:.4f} "
                f"does not beat champion r2={champion_r2_score:.4f}. "
                f"Keeping champion in production."
            )

            return False

        logging.info(
            f"Gate 3 PASSED: Challenger r2={challenger_r2_score:.4f} "
            f"> champion r2={champion_r2_score:.4f}. "
            f"Improvement: +{(challenger_r2_score - champion_r2_score):.4f}."
        )

    logging.info(
        f"All quality gates PASSED. "
        f"Challenger version={version} approved for promotion."
    )

    return True
    

def main():
    model_name = get_env("MLFLOW_MODEL_NAME") 
    alias = get_env("MLFLOW_MODEL_ALIAS")
    version = get_env("MLFLOW_MODEL_VERSION")

    client = MlflowClient()

    try:
        gates_passed = check_quality_gates(client=client, 
                                           model_name=model_name,
                                           version=version)
        if not gates_passed:
            sys.exit(1)  # WHY sys.exit(1): CI/CD reads exit codes.
                         # exit(1) = failure → pipeline stops
                         # exit(0) = success → pipeline continues

    except (RestException, MlflowException) as e:
        # WHY THIS IS NEEDED:
        # We are specifically catching the MLflow API error that occurs 
        # when a model or version does not exist in the registry.
        logging.error(f"MLflow Registry Error (Model '{model_name}' version '{version}' not found): {e}")
        sys.exit(1)
        
    except ValueError as e:
        # WHY SEPARATE VALUEERROR FROM GENERIC EXCEPTION:
        # This is a known, expected failure mode (no versions registered)
        # Handle it specifically so your logs are actionable
        logging.error(f"Configuration error: {e}")
        sys.exit(1)

    except Exception as e:
        raise CustomException(e, sys)
    
if __name__ == "__main__":
    main()

