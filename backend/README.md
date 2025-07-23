# RetailIQ Backend - ML-Powered Retail Analytics

A comprehensive machine learning backend for retail analytics that provides instant insights from CSV uploads.

## 🚀 Features

### Core ML Models

- **Customer Segmentation**: K-Means clustering for customer behavior analysis
- **Sales Forecasting**: Random Forest regression for future sales predictions
- **Churn Prediction**: ML-based customer churn risk assessment
- **Product Recommendations**: Collaborative filtering for cross-sell opportunities

### Traditional Analytics

- **Market Basket Analysis**: Apriori algorithm for association rules
- **Sales Forecasting**: Time series analysis with multiple models
- **Data Processing**: Upload and process CSV data files
- **RESTful API**: Comprehensive API endpoints for frontend integration

## Installation

1. **Create a virtual environment** (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Train ML Models** (First time only):

```bash
python ml_trainer.py
```

## Running the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## 📁 File Structure

```
backend/
├── app.py                      # Main Flask application
├── ml_trainer.py              # ML model training system
├── ml_predictor.py            # ML prediction engine
├── generate_large_dataset.py  # Dynamic dataset generator
├── demo_data_selector.py      # Demo data management
├── models/                    # Traditional analytics models
│   ├── apriori_market_basket.py
│   └── sales_forecaster.py
├── utils/                     # Utility functions
│   ├── data_processor.py
│   └── response_handler.py
├── trained_models/            # Pre-trained ML models
│   ├── retail_models.pkl
│   ├── encoders.pkl
│   ├── scalers.pkl
│   └── feature_importance.pkl
├── demo_data_*.csv           # Sample datasets
└── large_market_basket_data.csv # Main dynamic dataset
```

## API Endpoints

### 🤖 ML Analysis Endpoints

#### Instant CSV Analysis

```
POST /predict-analysis
Content-Type: multipart/form-data
Body: file (CSV file)
```

#### ML Insights

```
GET /ml-insights
```

#### Model Status

```
GET /ml-status
```

#### Train Models

```
POST /train-models
```

#### Customer Segmentation

```
GET /customer-segments
```

#### Churn Analysis

```
GET /churn-analysis
```

#### Product Recommendations

```
GET /product-recommendations
```

### 📊 Traditional Analytics

#### Health Check

```
GET /health
```

#### Data Upload

```
POST /upload-data
Content-Type: multipart/form-data
Body: file (CSV file)
```

### Market Basket Analysis

```
POST /market-basket-analysis
Content-Type: application/json
Body: {
  "min_support": 0.01,
  "min_confidence": 0.2,
  "min_lift": 1.0
}
```

### Get Recommendations

```
POST /get-recommendations
Content-Type: application/json
Body: {
  "items": ["Product A", "Product B"]
}
```

### Sales Forecast

```
POST /sales-forecast
Content-Type: application/json
Body: {
  "forecast_days": 30,
  "product": "Optional product filter",
  "category": "Optional category filter"
}
```

### Sales Trends

```
GET /sales-trends
```

### Data Summary

```
GET /data-summary
```

### Frequent Itemsets

```
POST /frequent-itemsets
Content-Type: application/json
Body: {
  "min_support": 0.01
}
```

## Data Format

The system expects CSV files with the following columns:

- `transaction_id`: Unique identifier for each transaction
- `date`: Transaction date
- `customer_id`: Customer identifier
- `product_name`: Name of the product
- `category`: Product category
- `quantity`: Quantity purchased
- `unit_price`: Price per unit

## Example Usage

### Python/JavaScript Frontend Integration

```javascript
// Upload data
const formData = new FormData();
formData.append("file", csvFile);

fetch("http://localhost:5000/upload-data", {
  method: "POST",
  body: formData,
})
  .then((response) => response.json())
  .then((data) => console.log(data));

// Get recommendations
fetch("http://localhost:5000/get-recommendations", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    items: ["Laptop", "Mouse"],
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data.data.recommendations));

// Get sales forecast
fetch("http://localhost:5000/sales-forecast", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    forecast_days: 30,
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data.data.forecasts));
```

## Machine Learning Models

### Market Basket Analysis

- **Algorithm**: Apriori algorithm via mlxtend library
- **Purpose**: Find frequent itemsets and association rules
- **Metrics**: Support, Confidence, Lift

### Sales Forecasting

- **Linear Regression**: Simple baseline model
- **Random Forest**: More sophisticated ensemble model
- **Moving Average**: Simple time series forecasting
- **Ensemble**: Combines multiple model predictions

## Configuration

Edit `config.py` to modify:

- CORS origins
- File upload limits
- Default model parameters
- Cache settings

## Development

### Project Structure

```
backend/
├── app.py                 # Main Flask application
├── run.py                 # Server startup script
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── models/
│   ├── __init__.py
│   ├── market_basket_analyzer.py
│   └── sales_forecaster.py
└── utils/
    ├── __init__.py
    ├── data_processor.py
    └── response_handler.py
```

### Adding New Features

1. Create new model classes in `models/` directory
2. Add new utility functions in `utils/` directory
3. Add new endpoints in `app.py`
4. Update requirements.txt if new dependencies are needed

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
2. **CORS errors**: Check that your frontend URL is listed in `config.py` CORS_ORIGINS
3. **File upload errors**: Ensure CSV files have the required columns
4. **Memory errors**: For large datasets, consider implementing data pagination

### Performance Tips

- Use smaller datasets for development
- Adjust min_support values for better performance in Apriori algorithm
- Consider caching results for repeated requests

## License

This project is part of the RetailIQ analytics platform.
