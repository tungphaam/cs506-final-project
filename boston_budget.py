import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score

class BostonBudgetPredictor:
    def __init__(self):
        self.scaler = RobustScaler()
        self.rf_model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.gb_model = GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=6,
            random_state=42
        )

    def preprocess_data(self, operating_df, capital_df):
        # Convert budget columns to numeric
        budget_columns = ['FY22 Actual Expense', 'FY23 Actual Expense', 'FY24 Appropriation', 'FY25 Budget']
        for col in budget_columns:
            operating_df[col] = pd.to_numeric(operating_df[col], errors='coerce')

        # Remove outliers
        for col in budget_columns:
            Q1 = operating_df[col].quantile(0.25)
            Q3 = operating_df[col].quantile(0.75)
            IQR = Q3 - Q1
            operating_df = operating_df[
                (operating_df[col] >= Q1 - 1.5 * IQR) & 
                (operating_df[col] <= Q3 + 1.5 * IQR)
            ]

        # Calculate growth rates
        operating_df['year_over_year_growth'] = (
            (operating_df['FY23 Actual Expense'] - operating_df['FY22 Actual Expense']) / 
            (operating_df['FY22 Actual Expense'] + 1e-6)
        ) * 100

        operating_df['budget_growth'] = (
            (operating_df['FY24 Appropriation'] - operating_df['FY23 Actual Expense']) / 
            (operating_df['FY23 Actual Expense'] + 1e-6)
        ) * 100

        # Group by department
        dept_features = operating_df.groupby('Dept').agg({
            'FY24 Appropriation': ['sum', 'mean'],
            'FY23 Actual Expense': ['sum', 'mean'],
            'budget_growth': 'mean',
            'year_over_year_growth': 'mean',
            'Expense Category': 'count'
        }).reset_index()

        # Flatten column names
        dept_features.columns = ['_'.join(col).strip() for col in dept_features.columns.values]

        # Process capital budget
        capital_features = capital_df.groupby('Department').agg({
            'Total_Project_Budget': 'sum',
            'Authorization_FY': 'sum',
            'External_Funds': 'sum'
        }).reset_index()

        # Merge features
        combined_features = pd.merge(
            dept_features,
            capital_features,
            left_on='Dept_',
            right_on='Department',
            how='left'
        ).fillna(0)

        return combined_features

    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train models
        self.rf_model.fit(X_train_scaled, y_train)
        self.gb_model.fit(X_train_scaled, y_train)
        
        # Get predictions
        rf_pred = self.rf_model.predict(X_test_scaled)
        gb_pred = self.gb_model.predict(X_test_scaled)
        ensemble_pred = 0.6 * rf_pred + 0.4 * gb_pred
        
        # Handle R² score calculation for small datasets
        # R² is undefined when there are fewer than two samples in the test set.
        if len(y_test) < 2:
            r2 = np.nan  # Assign nan for undefined R²
        else:
            r2 = r2_score(y_test, ensemble_pred)

        
        # Get cross-validation scores
        n_splits = min(5, len(X_train))
        cv_scores = cross_val_score(self.rf_model, X_train_scaled, y_train, cv=n_splits)
        
        return {
            'rmse': np.sqrt(mean_squared_error(y_test, ensemble_pred)),
            'r2': r2,
            'cv_scores_mean': cv_scores.mean(),
            'cv_scores_std': cv_scores.std(),
            'y_test': y_test,
            'predictions': ensemble_pred
        }


def main():
    operating_df = pd.read_csv("data/raw/operating_budget.csv")
    capital_df = pd.read_csv("data/raw/capital_budget.csv")
    
    predictor = BostonBudgetPredictor()
    features = predictor.preprocess_data(operating_df, capital_df)
    
    y = features['FY24 Appropriation_sum'] 
    feature_cols = [col for col in features.columns if col not in 
                   ['Dept_', 'Department', 'FY24 Appropriation_sum']]
    X = features[feature_cols]
    
    results = predictor.train_model(X, y)
    
    print(f"\nEnhanced Model Performance:")
    print(f"RMSE: ${results['rmse']:,.2f}")
    print(f"R2 Score: {results['r2']:.3f}")
    print(f"Cross-validation Score: {results['cv_scores_mean']:.3f} (+/- {results['cv_scores_std']:.3f})")

if __name__ == "__main__":
    main()