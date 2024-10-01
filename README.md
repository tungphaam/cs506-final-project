# Boston Budget Analysis Project

## Project Overview
This project aims to analyze the City of Boston’s annual budget to understand trends in spending and how they have evolved over time. The primary focus will be on the operating and capital budgets, with additional inisghts into spending per capita and per specific sectors such as education and public safety. The goal is to provide actionable insights that can help the City of Boston improve budget allocation and optimize spending.

## Project Goals
The main objectives are:
- Analyze how the City of Boston allocates its operating and capital budgets across departments, programs, and geographic areas.
- Understand changes in spending over time, especially in comparison to projected vs. actual spending.
- Provide insights into spending efficiency by calculating per capita and per program spending (e.g. per student in schools, per officer in public safety).
- Produce visualizations that make these insights accessible to stakeholders.

## Data Collection Plan
We will use publicly available datasets, including:
- **Operating Budget Data**: The detailed breakdown of the operating budget for the City of Boston. It should provide information on the budget allocations for different departments, services, and personnel expenses such as teachers, police officers, and firefighters.
    - [OPERATING BUDGET](https://data.boston.gov/dataset/operating-budget/resource/8f2971f0-7a0d-401d-8376-0289e3b810ba)
- **Capital Budget Data**: The capital budget for the City of Boston, specifying the funding sources, project descriptions, and budget allocations for acquiring or improving physical assets owned by the city.
    - [CAPITAL BUDGET](https://data.boston.gov/dataset/capital-budget/resource/c62d666e-27ea-4c03-9cb1-d3a81a1fb641)
- **Supplementary Socioeconomic Data**: Social Vulnerability Index and census data for Boston neighborhoods to explore correlations with budget allocations.

## Modeling Approach
- **Data Cleaning**: Address missing values and standardize datasets from different sources.
- **Feature Extraction**: Calculate per capita spending, department-specific allocations, and program-level expenditures.
- **Modeling**: Apply clustering to group departments based on spending trends and use linear models to predict future spending based on historical data.
- **Visualization**: Create interactive and static visualizations using Power BI and Python (Matplotlib/Seaborn).

## Visualizations
We plan to generate at least 5-7 visualizations:
- **Bar charts**: Departmental budgets over time.
- **Heatmaps**: Geographic distribution of funds.
- **Line charts**: Comparison of projected vs. actual spending.
- **Scatter plots**: Correlations between per capita spending and socioeconomic factors. 

## Testing Plan
- **Train/Test Split**: Use 80/20 split of historical data to train and test the model, ensuring accurate predictions.
- **Cross-Validation**: Apply k-fold cross validation to avoid overfitting and assess model robustness.
- **Data Validation**: Cross-check the model's results with external datasets (e.g., socioeconomic factors, census data).
- **Performance Metrics**: Use MAE, RMSE, and R^2 for regression analysis; use accuracy and F1-score for classification problems.
- **Error Analysis**: Investigate prediction errors by department or budget category, and analyze feature importance to improve the model.

## Timeline
- **October 1**: Proposal submission
- **October 15**: Data Collection & Cleaning
- **October 25**: Feature Extraction
- **November 1**: Initial Insights & Visualizations
- **November 5**: Midterm Report & Presentation
- **November 12**: Model Development
- **November 25**: Model Testing and Evaluation
- **December 10**: Final Report & Presentation