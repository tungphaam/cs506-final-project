# Boston Budget Analysis Project

[Youtube Link](https://youtu.be/fBA2DA9J3i8)

---

## Project Overview
This project aims to analyze the City of Boston’s annual budget to understand trends in spending and how they have evolved over time. The primary focus will be on the operating and capital budgets, with additional insights into spending per capita and per specific sectors such as education and public safety. The goal is to provide actionable insights that can help the City of Boston improve budget allocation and optimize spending.

## Project Goals
The main objectives are:
- Analyze how the City of Boston allocates its operating and capital budgets across departments, programs, and geographic areas.
- Understand changes in spending over time, especially in comparison to projected vs. actual spending.
- Provide insights into spending efficiency by calculating per capita and per program spending (e.g. per student in schools, per officer in public safety).
- Produce visualizations that make these insights accessible to stakeholders.

---

## 1. Data Processing

### Data Collection

We will use publicly available datasets, including:
- **Operating Budget Data**: The detailed breakdown of the operating budget for the City of Boston. It should provide information on the budget allocations for different departments, services, and personnel expenses such as teachers, police officers, and firefighters.
    - [OPERATING BUDGET](https://data.boston.gov/dataset/operating-budget/resource/8f2971f0-7a0d-401d-8376-0289e3b810ba)
- **Capital Budget Data**: The capital budget for the City of Boston, specifying the funding sources, project descriptions, and budget allocations for acquiring or improving physical assets owned by the city.
    - [CAPITAL BUDGET](https://data.boston.gov/dataset/capital-budget/resource/c62d666e-27ea-4c03-9cb1-d3a81a1fb641)
- **Supplementary Socioeconomic Data**: Social Vulnerability Index and census data for Boston neighborhoods to explore correlations with budget allocations.

### Data Cleaning

The initial data require extensive cleaning to ensure consistency and usability:
- **Handling Missing Values:** Missing values were replaced with appropriate placeholders, and missing indicators (e.g., `#Missing`) were standardized or filled.
- **Standardizing Column Names:** Columns were renamed for consistency and readability, converting names to lowercase and replacing spaces with underscores.
- **Data Type Corrections:** Numeric fields were converted from string to float where necessary to allow for calculations and visualizations.

### Feature Extraction 

To better analyze budget allocations, we extracted key features from the data:
- **Per Capital Spending:** Represents per capita spending for each year, to see how much the city spends per resident by department.
- **Department-Specific Allocations:** Analyzes how much each department receives within total budget, both as an absolute amount and as a percentage of the total budget.
- **Program-Level Expenditures:** Analyzes spending at the program level, which can provide insights into how much is allocated to specific initiatives or services within each department.
- **Year-over-year Budget Growth:** Calculates the growth rate of each budget from year to year.
- **Average Spending Per Program:** Calculates the average spending per program across all departments to get a sense of typical program costs. 

---

## 2. Data Modeling Methods

### Clustering

To categorize programs and departments based on budget allocations, we used **clustering analysis:**
- **Approach:** We applied clustering on FY24 and FY25 budget data to group programs with similar budget characteristics. This grouping allows us to understand  which programs are high, medium, or low priority in terms of budget allocations.
-**Insights:** Programs were grouped into 3 clusters: high-budget, medium-budget, and low-budget groups, reflecting Boston's allocation priorities.

---

## 3. Preliminary Visualizations and Insights

### Visualization 1: Total Budget by Department (FY25)

- **Description**: This bar chart shows the FY25 budget allocations across the top 10 departments.
- **Insight**: Boston Public Schools have the largest allocation, emphasizing the city’s focus on education. Other high-budget departments include the Police Department and Pensions, which reflect Boston’s investment in public safety and employee benefits.

### Visualization 2: Budget Growth Over Fiscal Years

- **Description**: A line chart showing budget growth from FY22 to FY25.
- **Insight**: There’s a steady increase in the budget over time, with a notable jump in FY25. This may indicate planned expansions in services or increased revenues, signaling Boston’s commitment to meeting growing city needs.

### Visualization 3: Per Capita Spending by Department (FY25)

- **Description**: A horizontal bar chart displaying per capita spending across the top 10 departments.
- **Insight**: Boston Public Schools receive the highest per capita spending, indicating a focus on providing substantial resources per resident for education. The Police Department and Pensions follow, highlighting priorities in safety and long-term commitments to employee welfare.

### Visualization 4: Top Programs by FY25 Budget

- **Description**: A bar chart of the top 10 programs by FY25 budget.
- **Insight**: The highest-funded programs include Pensions, BPS Operations, and Charter School Tuition, reflecting commitments to employee benefits and a substantial investment in both public and charter schools.

### Visualization 5: Clustering of Programs Based on Budget Allocations

- **Description**: Scatter plot showing clusters of programs based on FY24 and FY25 budget allocations.
- **Insight**: The clustering reveals three distinct groups (high, medium, and low budget allocations). High-budget programs are likely essential city priorities, while lower-budget programs may represent administrative functions or smaller initiatives.

---

## 4. Preliminary Results

### Key Findings

1. **Education and Public Safety as Priorities**
   - Boston Public Schools consistently receive the largest share of the budget, reflecting the city’s strong focus on education.
   - The Police Department also has a high allocation, along with the Fire Department and other public safety-related areas.

2. **Consistent Budget Growth**
   - The budget has grown consistently over the years, indicating Boston’s commitment to expanding or maintaining services to meet population needs. This growth supports both core services and long-term financial obligations.

3. **Clustered Spending Patterns**
   - The clustering analysis grouped programs into high, medium, and low-budget categories, providing insights into the city’s funding priorities and allowing for strategic comparisons across programs. High-budget clusters reflect Boston's main priorities, while low-budget clusters may indicate more auxiliary or administrative services.

4. **Per Capita Insights**
   - Calculating per capita spending offered a unique perspective on how each resident’s tax dollars are allocated across departments, with the highest per capita spending in education and public safety.

---

## 5. Predictive Modeling

### Approach and Implementation
Our predictive modeling approach uses an ensemble method combining two powerful algorithms:

1. **Random Forest Regressor**
   - Configuration:
     - 200 decision trees
     - Maximum depth of 10 levels
     - Minimum 5 samples for node splitting
     - Minimum 2 samples per leaf
     - Optimized for balanced accuracy and complexity
   - Purpose: Captures complex non-linear relationships in budget allocations

2. **Gradient Boosting Regressor**
   - Configuration:
     - 200 sequential trees
     - Learning rate of 0.05 for gradual improvements
     - Maximum depth of 6 to prevent overfitting
   - Purpose: Improves predictions through iterative error correction

### Model Tuning
1. **Data Preprocessing**
   - Robust scaling of features to handle outliers
   - Removal of outliers using IQR method
   - Feature engineering including:
     - Growth rate calculations
     - Department-level aggregations
     - Capital budget integrations

2. **Ensemble Weighting**
   - Random Forest: 60% contribution
   - Gradient Boosting: 40% contribution
   - Weights determined through cross-validation performance

### Model Performance Analysis

1. **Key Metrics**
   - RMSE: $270,729.96 (average prediction error)
   - R² Score: 0.933 (93.3% variance explained)
   - Cross-validation Score: 0.720 (±0.169)

2. **Feature Importance**
   The model identified five key predictive features:
   ```
   Feature                    Importance
   FY23 Actual Expense_sum    0.722303
   Expense Category_count     0.179095
   FY24 Appropriation_mean    0.064829
   FY23 Actual Expense_mean   0.016086
   Authorization_FY           0.009849
   ```

   Analysis of feature importance reveals:
   - Historical spending (FY23 Actual Expense) is the strongest predictor at 72.2%
   - Department complexity (Expense Categories) accounts for 17.9%
   - Current appropriations contribute 6.5%
   - Mean expenses and fiscal year authorizations have minor influences

3. **Visualization Analysis**
   - Feature Importance Plot shows clear hierarchy of predictive factors
   - Actual vs Predicted Plot demonstrates:
     - Strong alignment along the perfect prediction line
     - Higher variance in predictions for larger budgets
     - Consistent accuracy across most budget ranges

### Model Strengths and Limitations

1. **Strengths**
   - High predictive accuracy (93.3% R² score)
   - Robust cross-validation performance
   - Clear feature importance interpretability
   - Good handling of department-level variations

2. **Limitations**
   - Increased uncertainty for larger budget predictions
   - Moderate cross-validation standard deviation (±0.169)
   - Limited utilization of capital budget features
   - Potential for overfitting in specific department categories

### Implementation Results
The model demonstrates strong capability in predicting departmental budgets, with particularly good performance in:
- Mid-range budget predictions
- Department-level allocations
- Year-over-year growth patterns

The high R² score and reasonable RMSE indicate that the model can be a valuable tool for budget planning and analysis, though careful consideration should be given to predictions for extremely large budgets where uncertainty increases.

---

## 6. Future Work

1. **Enhanced Feature Engineering for Capital Budget Integration**:
   - Develop more sophisticated metrics to combine operating and capital budgets:
      - Design new ratios to measure the relationship between operational spending and capital project outcomes
      - Build time-series features that capture the long-term impact of capital investments on operational costs
   - Create neighborhood-specific impact scores for capital investments

2. **Geographic Analysis of Budget Distribution**:
   - Map budget allocations across Boston's neighborhoods to identify potential spending disparities
   - Create interactive visualizations showing:
      - Per Capita spending by neighborhood
      - Distribution of capital projects across different areas
      - Infrastructure investment patterns
   - Analyze the relationship between neighborhood characteristics and budget allocation

3. **Socioeconomic Factor Correlation Analysis**:
   - Integrate demographic data to understand spending patterns:
      - Population density impact on service delivery costs
      - Income level correlations with public service needs
      - Age distribution effects on program requirements
   - Study the relationship between:
      - Educational outcomes and school budget allocation
      - Crime rates and public safety spending
      - Public health metrics and healthcare investments
   - Analyze how social vulnerability indices correlate with budget priorities

4. **Enhanced Machine Learning Applications**:
   - Implement more sophisticated models:
      - Deep learning for complex pattern recognition
      - Neural networks for multi-variable prediction
      - Time series models for trend analysis
   - Develop automated anomaly detection systems for:
      - Unusual spending patterns
      - Budget inefficiencies
      - Potential cost savings opportunities

## Timeline
- **October 1**: Proposal submission
- **October 15**: Data Collection & Cleaning
- **October 25**: Feature Extraction
- **November 1**: Initial Insights & Visualizations
- **November 5**: Midterm Report & Presentation
- **November 12**: Model Development
- **November 25**: Model Testing and Evaluation
- **December 10**: Final Report & Presentation