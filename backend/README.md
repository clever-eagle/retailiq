# Retail Analytics Backend

A Python Flask backend service that provides AI-powered retail analytics including market basket analysis using the Apriori algorithm and sales forecasting.

## Features

- **Market Basket Analysis**: Uses Apriori algorithm to find frequent itemsets and association rules
- **Product Recommendations**: Get product recommendations based on current items in cart
- **Sales Forecasting**: Multiple forecasting models including Linear Regression, Random Forest, and time series analysis
- **Data Processing**: Upload and process CSV data files
- **RESTful API**: Clean API endpoints for frontend integration

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

## Running the Server

### Option 1: Using the run script

```bash
python run.py
```

### Option 2: Using Flask directly

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check

```
GET /health
```

### Data Upload

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
