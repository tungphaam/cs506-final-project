from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
from boston_budget import BostonBudgetPredictor
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load and process data once at startup
operating_df = pd.read_csv("data/raw/operating_budget.csv")
capital_df = pd.read_csv("data/raw/capital_budget.csv")
predictor = BostonBudgetPredictor()
features = predictor.preprocess_data(operating_df, capital_df)

# Constants
BOSTON_POPULATION = 654423

# Train model
y = features['FY24 Appropriation_sum']
feature_cols = [col for col in features.columns if col not in ['Dept_', 'Department', 'FY24 Appropriation_sum']]
X = features[feature_cols]
model_results = predictor.train_model(X, y)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/top-departments')
def top_departments():
    dept_budgets = features.nlargest(10, 'FY24 Appropriation_sum')
    return jsonify({
        'departments': dept_budgets['Dept_'].tolist(),
        'budgets': dept_budgets['FY24 Appropriation_sum'].tolist()
    })

@app.route('/api/budget-growth')
def budget_growth():
    yearly_budget = operating_df.groupby('Dept')[
        ['FY22 Actual Expense', 'FY23 Actual Expense', 'FY24 Appropriation']
    ].sum().mean()
    
    return jsonify({
        'years': ['FY22', 'FY23', 'FY24'],
        'budgets': yearly_budget.tolist()
    })

@app.route('/api/per-capita-spending')
def per_capita_spending():
    per_capita = features.nlargest(10, 'FY24 Appropriation_sum')
    per_capita['per_capita'] = per_capita['FY24 Appropriation_sum'] / BOSTON_POPULATION
    
    return jsonify({
        'departments': per_capita['Dept_'].tolist(),
        'spending': per_capita['per_capita'].tolist()
    })

@app.route('/api/program-expenditures')
def program_expenditures():
    program_budget = operating_df.groupby(['Dept', 'Program'])['FY24 Appropriation'].sum()
    top_programs = program_budget.nlargest(10)
    
    return jsonify({
        'programs': top_programs.index.get_level_values(1).tolist(),
        'budgets': top_programs.values.tolist()
    })

@app.route('/api/budget-share')
def budget_share():
    total_budget = features['FY24 Appropriation_sum'].sum()
    dept_share = features.nlargest(10, 'FY24 Appropriation_sum')
    dept_share['share'] = dept_share['FY24 Appropriation_sum'] / total_budget * 100
    
    return jsonify({
        'departments': dept_share['Dept_'].tolist(),
        'shares': dept_share['share'].tolist()
    })

@app.route('/api/program-clusters')
def program_clusters():
    # Prepare data for clustering
    program_data = operating_df.groupby('Program')[
        ['FY22 Actual Expense', 'FY23 Actual Expense', 'FY24 Appropriation']
    ].sum()
    
    # Standardize features
    scaler = StandardScaler()
    program_data_scaled = scaler.fit_transform(program_data)
    
    # Apply clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(program_data_scaled)
    
    return jsonify({
        'x': program_data['FY24 Appropriation'].tolist(),
        'y': program_data['FY23 Actual Expense'].tolist(),
        'clusters': clusters.tolist(),
        'programs': program_data.index.tolist()
    })

@app.route('/api/model-performance')
def model_performance():
    return jsonify({
        'metrics': {
            'rmse': float(model_results['rmse']),
            'r2': float(model_results['r2']),
            'cv_score': float(model_results['cv_scores_mean']),
            'cv_std': float(model_results['cv_scores_std'])
        },
        'feature_importance': dict(zip(feature_cols, predictor.rf_model.feature_importances_))
    })

@app.route('/api/prediction-analysis')
def prediction_analysis():
    # Use the results from the already trained model
    return jsonify({
        'actual': model_results['y_test'].tolist(),
        'predicted': model_results['predictions'].tolist()
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)
