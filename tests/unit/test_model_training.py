from pathlib import Path
import numpy as np
import pytest
import json
from mlops.components.model_training import Training


# SYNTHETIC GROUND TRUTH TEST
def _make_synthetic_train_array(config, n_samples=50, n_features=3, seed=0):
    """Pure numpy array, not derived from any preprocessor."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n_samples, n_features))
    true_coef = rng.normal(size=n_features)
    y = X @ true_coef + rng.normal(scale=0.1, size=n_samples)  # near-linear, low noise
    arr = np.column_stack([X, y])
    saved_path = config.train_data_file
    np.save(saved_path, arr)


@pytest.fixture
def prepared_model_training_config(model_training_config):
    _make_synthetic_train_array(config=model_training_config)
    return model_training_config


def test_train_sets_is_trained_flag(prepared_model_training_config):
    trainer = Training(config=prepared_model_training_config)
    trainer.train()
    assert trainer._is_trained is True


def test_train_fits_a_linear_regression_with_expected_coef_shape(prepared_model_training_config):
    trainer = Training(config=prepared_model_training_config)
    trainer.train()
    assert trainer.lr.coef_.shape == (3,)  # matches n_features


def test_evaluate_raises_if_called_before_train(prepared_model_training_config):
    trainer = Training(config=prepared_model_training_config)
    # with pytest.raises(RuntimeError, match="train\\(\\) before evaluate\\(\\)"):
    with pytest.raises(RuntimeError, match=r"train\(\) before evaluate\(\)\."):
        trainer.evaluate()


def test_evaluate_produces_near_perfect_r2_on_near_linear_synthetic_data(prepared_model_training_config):
    trainer = Training(config=prepared_model_training_config)
    trainer.train()
    trainer.evaluate()
    
    report = json.loads(Path(prepared_model_training_config.model_report).read_text())
    # Since y is constructed as a near-perfect linear function of X,
    # a correctly-fit LinearRegression should explain almost all variance.
    assert report["train"]["r2_score"] > 0.95