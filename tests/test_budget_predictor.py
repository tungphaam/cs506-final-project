import pytest
import pandas as pd
import numpy as np
from boston_budget import BostonBudgetPredictor
import math

# Sample data for testing
@pytest.fixture
def sample_data():
    """Fixture to generate sample data for testing."""
    np.random.seed(42)  # Ensure reproducibility
    n_samples = 50
    departments = ['A', 'B', 'C', 'D', 'E'] * 10

    # Create sample operating budget data
    operating_df = pd.DataFrame({
        'Dept': departments[:n_samples],
        'FY22 Actual Expense': np.random.uniform(100, 1000, n_samples),
        'FY23 Actual Expense': np.random.uniform(120, 1200, n_samples),
        'FY24 Appropriation': np.random.uniform(150, 1500, n_samples),
        'FY25 Budget': np.random.uniform(200, 2000, n_samples),
        'Expense Category': ['Cat1', 'Cat2', 'Cat3', 'Cat4', 'Cat5'] * 10
    })

    # Create sample capital budget data
    capital_df = pd.DataFrame({
        'Department': ['A', 'B', 'C', 'D', 'E'],
        'Total_Project_Budget': np.random.uniform(1000, 5000, 5),
        'Authorization_FY': np.random.uniform(500, 2500, 5),
        'External_Funds': np.random.uniform(200, 1000, 5)
    })

    return operating_df, capital_df

# Test cases

def test_predictor_initialization():
    """Test that the predictor initializes correctly."""
    predictor = BostonBudgetPredictor()
    assert predictor is not None, "Predictor instance is None."
    assert predictor.rf_model is not None, "Random Forest model is not initialized."
    assert predictor.gb_model is not None, "Gradient Boosting model is not initialized."

def test_data_preprocessing(sample_data):
    """Test the data preprocessing step."""
    operating_df, capital_df = sample_data
    predictor = BostonBudgetPredictor()
    features = predictor.preprocess_data(operating_df, capital_df)

    # Check if features DataFrame is created correctly
    assert isinstance(features, pd.DataFrame), "Features should be a DataFrame."
    assert len(features) > 0, "Features DataFrame is empty."
    assert 'FY24 Appropriation_sum' in features.columns, "Missing column: FY24 Appropriation_sum."
    assert 'FY23 Actual Expense_sum' in features.columns, "Missing column: FY23 Actual Expense_sum."

def test_model_training(sample_data):
    """Test the model training process."""
    operating_df, capital_df = sample_data
    predictor = BostonBudgetPredictor()
    features = predictor.preprocess_data(operating_df, capital_df)

    # Prepare features and target for training
    y = features['FY24 Appropriation_sum']
    feature_cols = [col for col in features.columns if col not in ['Dept_', 'Department', 'FY24 Appropriation_sum']]
    X = features[feature_cols]

    # Test model training
    results = predictor.train_model(X, y)

    # Check if results contain expected metrics
    for metric in ['rmse', 'r2', 'cv_scores_mean', 'cv_scores_std']:
        assert metric in results, f"Missing metric: {metric}."

    # Check if metrics are within reasonable ranges
    assert results['rmse'] >= 0, "RMSE should be non-negative."

    # Handle potential nan for R²
    if math.isnan(results['r2']):
        assert len(results['y_test']) < 2, "R2 should only be nan for datasets with less than two test samples."
    else:
        assert 0 <= results['r2'] <= 1, "R2 should be between 0 and 1."

def test_feature_engineering(sample_data):
    """Test the feature engineering step."""
    operating_df, capital_df = sample_data
    predictor = BostonBudgetPredictor()
    features = predictor.preprocess_data(operating_df, capital_df)

    # Test required columns exist
    required_columns = [
        'FY24 Appropriation_sum',
        'FY23 Actual Expense_sum',
        'budget_growth_mean',
        'year_over_year_growth_mean'
    ]

    for col in required_columns:
        assert col in features.columns, f"Missing column: {col}."

def test_model_predictions(sample_data):
    """Test the model's predictions."""
    operating_df, capital_df = sample_data
    predictor = BostonBudgetPredictor()
    features = predictor.preprocess_data(operating_df, capital_df)

    # Prepare features and target for training
    y = features['FY24 Appropriation_sum']
    feature_cols = [col for col in features.columns if col not in ['Dept_', 'Department', 'FY24 Appropriation_sum']]
    X = features[feature_cols]

    # Train model
    results = predictor.train_model(X, y)

    # Check predictions are reasonable
    assert results['rmse'] > 0, "RMSE should be positive."
    assert not np.isinf(results['rmse']), "RMSE should not be infinite."
    assert not np.isnan(results['rmse']), "RMSE should not be NaN."
