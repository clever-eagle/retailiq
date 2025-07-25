# Backend overview: 

## System Architecture: 

#### 1. Backend Techstack: 
- **Flask (framework)**: Backend is done using Flask:
  
  in `backend/app.py`, backend is initialized using flask: 
  ```
  from flask import Flask, request, jsonify
  app = Flask(__name__)
  ```

- **RESTful API (api style)**: 
  - Backend uses API endpoints that uses RESTful API style
  - API endpoints are: 
    - `/data-summary`
    - `/upload-data`
    - `/current-analysis`
    - `/market-basket-analysis`

- **Python libraries and frameworks:**
  - **pandas**: 
    - Reading CSV files for uploading sales data. 
    - Data aggregation, filtering and preparation: 
      - Cleaning, validating and transforming data into DataFrames. 
      - Grouping sales data by product, date, category to calculate totals & trends.
      - Filtering rows based on conditions (e.g., data ranges, product ytpes) for targeted analysis.
      - Selecting and transforming columns to create datasets needed for forecasting vs market-basket analysis
      - Preparing cleaned DataFrames as input for ML models 
      - Calculating metrics such : 
        - Total sales per product, category or date
        - Top-selling products
        - Sales trends over time (daily, weekly, monthly)
        - Average transaction value
        - Number of transactions
        - Product frequency for market basket analysis
        - Summary statistics (mean, sum, count, min, max) for sales and transactions. 

        **These metrics are used for dashboard summaries, analytics and as input for forecasting and market-basket modules**
  - **NumPy**: 
    - Perform numerical operations: 
      - Used for generating random numbers and synthetic data: 
        - Random sales amounts, dates, or product selections for sample datasets. 
    - Array computations: 
      - Used for efficient mathematical operations on arrays: 
        - Array summing, averaging, and other calculations that support data analysis and preprocessing. 
    - Integration with `pandas`: 
      - Supports pandas DataFrame operations by providing fast, vectorized computations and enabling complex data manipulations (e.g., applying NumPy functions to DataFrame columns)
    - Statistical analysis: 
      - Assists in calculating metrics like mean, standard deviation, and other statistical summaries for analytics and model input prepartion. 
    - Machine learning preprocessing: 
      - Used for transforming and scaling data before feeding it into ML models
      - To ensure data consistency and model perform better by removing the dataset's large numbers and unusual properties. 
  - **scikit-learn:**
    - A python library for ML
    - Provides tools for data preprocessing, model training (classification, regression, clustering), evaluation. 
    - Used for: 
      - Training models:
        - Random Forest (for classification/regression tasks)
        - KMeans (clustering analysis)
      - Scaling and transforming data before model training: 
        - Using `StandardScaler` to normalize numerical features, ensuring all input data is on a similar scale before training models.
      - Encoding categorical variables: 
        - Categorical data is converted into numerical format using `LabelEncoder`, so ML models can process them. 
      - Evaluating metrics: 
        - RMSE, MAE, MSE and R²j
  - **Pickle:**
    - Picke is a Python library used to serialize (save) and deserialize (load) Python objects to and from files. 
    - Allows to store trained models, data preprocessors, and other python objects and reuse them later without retraining/recalculating. 
    - Implementation: 
      - Pickle file is used to save trained ML models like Random Forest(), encoders and scales as `.pkl` files after training: 
      - Use these `.pkl` files in backend to use the model to process new data without retraining the models. 
      - Usage: 
        - In `ml_trainer.py`:
          - Purpose: Save trained ML models, encoders, scalers and feature importance dictionaries to disk after training.
          - Implementation: 
             - `pickle.dump()` to serialize and store the models as `.pkl` files in `trained_models` directory
             - `picle.load()` to load the model for later use to avoid retraining. 
        - In `ml_predictor.py`: 
          - Purpose: Load pre-trained models and preprocessors for instant analysis of new data uploads. 
          - Implementation: 
            - `pickle.load()`: to load the models, encoders, scales from `.pkl` files. 
  - **Apriori (AI Model):**
    - What it does: 
      - **Purpose**: The apriori model is used for Market Basket Analysis (MBA) to discover frequent itemsets and generate association rules from retail transaction data. 
      - **Business Value**: It helps to identify products often bought together, enabling cross-selling, bundling, and product recommendation strategies. 
    - How it works: 
      - **Algorithm**: 
        - The Apriori algorithm finds frequent itemsets in transaction data by iteratively expanding item combinations and pruning infrequent ones. It then generates association rules with metrics like support, confidence and lift. 
        - **Workflow:** 
          - Data Preparation: Transaction data is grouped by transaction ID, forming basket of items. 
          - Frequent itemset mining: The algorithm finds itemsets that meet a minimum support threshold. 
          - Rule Generation: Association rules are created from frequent itemsets, filtered by minimum confidence and lift. 
    - Implementation: 
      - `apriori_market_basket.py`: contains the main implmentation
    - Integration: 
      - The backend exposes REST API endpoint `/market-basket-analysis` that triggers the class `AprioriMarketBasket` from `apriori_market_basket.py` and generates association rules using methods from that file. 
      - The React frontend calls the backend API, recevies association rules and itemsets, and displays the output. 

## File Structure:
