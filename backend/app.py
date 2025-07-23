from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from models.apriori_market_basket import AprioriMarketBasket
from models.sales_forecaster import SalesForecaster
from utils.data_processor import DataProcessor
from utils.response_handler import ResponseHandler
from ml_trainer import RetailMLTrainer
from ml_predictor import RetailMLPredictor

app = Flask(__name__)
CORS(app)

# Initialize models
apriori_analyzer = AprioriMarketBasket()
sales_forecaster = SalesForecaster()
data_processor = DataProcessor()
response_handler = ResponseHandler()

# Initialize ML components
ml_trainer = RetailMLTrainer()
ml_predictor = RetailMLPredictor()

# Store for uploaded data
uploaded_data = None


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/upload-data", methods=["POST"])
def upload_data():
    """Upload CSV data for analysis"""
    try:
        if "file" not in request.files:
            return response_handler.error("No file provided", 400)

        file = request.files["file"]
        if file.filename == "":
            return response_handler.error("No file selected", 400)

        if not file.filename.endswith(".csv"):
            return response_handler.error("File must be a CSV", 400)

        # Process the uploaded file
        df = pd.read_csv(file)
        global uploaded_data
        uploaded_data = data_processor.validate_and_clean_data(df)

        return response_handler.success(
            {
                "message": "Data uploaded successfully",
                "rows": len(uploaded_data),
                "columns": list(uploaded_data.columns),
            }
        )

    except Exception as e:
        return response_handler.error(f"Upload failed: {str(e)}", 500)


@app.route("/market-basket-analysis", methods=["POST"])
def market_basket_analysis():
    """Perform market basket analysis using Apriori algorithm"""
    try:
        data = request.get_json()
        min_support = data.get("min_support", 0.01)
        min_confidence = data.get("min_confidence", 0.2)
        min_lift = data.get("min_lift", 1.0)

        # Use uploaded data or default data
        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available for analysis", 400)

        # Perform market basket analysis
        results = apriori_analyzer.analyze(
            df,
            min_support=min_support,
            min_confidence=min_confidence,
            min_lift=min_lift,
        )

        return response_handler.success(results)

    except Exception as e:
        return response_handler.error(f"Market basket analysis failed: {str(e)}", 500)


@app.route("/get-recommendations", methods=["POST"])
def get_recommendations():
    """Get product recommendations based on current items in cart"""
    try:
        data = request.get_json()
        current_items = data.get("items", [])

        if not current_items:
            return response_handler.error("No items provided", 400)

        # Use uploaded data or default data
        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available for recommendations", 400)

        # Load data into the analyzer and generate rules
        apriori_analyzer.load_transactions(df)
        apriori_analyzer.find_frequent_itemsets(min_support=0.01)
        apriori_analyzer.generate_association_rules(min_confidence=0.2, min_lift=1.0)

        recommendations = apriori_analyzer.get_recommendations(current_items)

        return response_handler.success(
            {"current_items": current_items, "recommendations": recommendations}
        )

    except Exception as e:
        return response_handler.error(f"Recommendation failed: {str(e)}", 500)


@app.route("/sales-forecast", methods=["POST"])
def sales_forecast():
    """Generate sales forecast"""
    try:
        data = request.get_json()
        forecast_days = data.get("forecast_days", 30)
        product_filter = data.get("product", None)
        category_filter = data.get("category", None)

        # Use uploaded data or default data
        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available for forecasting", 400)

        forecast_result = sales_forecaster.forecast(
            df,
            forecast_days=forecast_days,
            product_filter=product_filter,
            category_filter=category_filter,
        )

        return response_handler.success(forecast_result)

    except Exception as e:
        return response_handler.error(f"Sales forecasting failed: {str(e)}", 500)


@app.route("/sales-trends", methods=["GET"])
def sales_trends():
    """Get sales trends analysis"""
    try:
        # Use uploaded data or default data
        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available for trends analysis", 400)

        trends = sales_forecaster.get_trends(df)

        return response_handler.success(trends)

    except Exception as e:
        return response_handler.error(f"Trends analysis failed: {str(e)}", 500)


@app.route("/data-summary", methods=["GET"])
def data_summary():
    """Get summary of available data"""
    try:
        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available", 400)

        summary = data_processor.get_data_summary(df)

        return response_handler.success(summary)

    except Exception as e:
        return response_handler.error(f"Data summary failed: {str(e)}", 500)


@app.route("/frequent-itemsets", methods=["POST"])
def frequent_itemsets():
    """Get frequent itemsets"""
    try:
        data = request.get_json()
        min_support = data.get("min_support", 0.01)

        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available for analysis", 400)

        # Load data into the analyzer first
        apriori_analyzer.load_transactions(df)
        apriori_analyzer.find_frequent_itemsets(min_support)

        itemsets = apriori_analyzer.get_formatted_frequent_itemsets()

        return response_handler.success(
            {"frequent_itemsets": itemsets, "min_support": min_support}
        )

    except Exception as e:
        return response_handler.error(
            f"Frequent itemsets analysis failed: {str(e)}", 500
        )


@app.route("/train-models", methods=["POST"])
def train_models():
    """Train ML models on existing data"""
    try:
        print("🚀 Starting ML model training...")

        # Train all models
        training_results = ml_trainer.train_all_models()

        return response_handler.success(
            {
                "message": "ML models trained successfully",
                "training_results": training_results,
            }
        )

    except Exception as e:
        return response_handler.error(f"Model training failed: {str(e)}", 500)


@app.route("/predict-analysis", methods=["POST"])
def predict_analysis():
    """Analyze uploaded CSV using pre-trained ML models"""
    try:
        if "file" not in request.files:
            return response_handler.error("No file provided", 400)

        file = request.files["file"]
        if file.filename == "":
            return response_handler.error("No file selected", 400)

        if not file.filename.endswith(".csv"):
            return response_handler.error("File must be a CSV", 400)

        print(f"📁 Analyzing uploaded file: {file.filename}")

        # Read the uploaded CSV
        df = pd.read_csv(file)

        # Use ML predictor to analyze the data
        analysis_results = ml_predictor.analyze_new_data(df)

        # Store the uploaded data globally for other endpoints
        global uploaded_data
        uploaded_data = ml_predictor._validate_data(df)

        return response_handler.success(
            {
                "message": "CSV analyzed successfully with ML models",
                "analysis": analysis_results,
                "file_info": {
                    "filename": file.filename,
                    "records": len(df),
                    "columns": list(df.columns),
                },
            }
        )

    except Exception as e:
        return response_handler.error(f"ML analysis failed: {str(e)}", 500)


@app.route("/ml-insights", methods=["GET"])
def ml_insights():
    """Get ML insights for currently loaded data"""
    try:
        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available for analysis", 400)

        # Generate ML insights
        analysis_results = ml_predictor.analyze_new_data(df)

        return response_handler.success(analysis_results)

    except Exception as e:
        return response_handler.error(f"ML insights failed: {str(e)}", 500)


@app.route("/customer-segments", methods=["GET"])
def get_customer_segments():
    """Get customer segmentation results"""
    try:
        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available", 400)

        # Get customer segments from ML predictor
        results = ml_predictor._predict_customer_segments(df)

        return response_handler.success(results)

    except Exception as e:
        return response_handler.error(f"Customer segmentation failed: {str(e)}", 500)


@app.route("/churn-analysis", methods=["GET"])
def get_churn_analysis():
    """Get customer churn analysis"""
    try:
        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available", 400)

        # Get churn analysis from ML predictor
        results = ml_predictor._predict_churn(df)

        return response_handler.success(results)

    except Exception as e:
        return response_handler.error(f"Churn analysis failed: {str(e)}", 500)


@app.route("/product-recommendations", methods=["GET"])
def get_product_recommendations():
    """Get AI-powered product recommendations"""
    try:
        df = (
            uploaded_data
            if uploaded_data is not None
            else data_processor.load_default_data()
        )

        if df is None:
            return response_handler.error("No data available", 400)

        # Get product recommendations from ML predictor
        results = ml_predictor._get_product_recommendations(df)

        return response_handler.success(results)

    except Exception as e:
        return response_handler.error(f"Product recommendations failed: {str(e)}", 500)


@app.route("/ml-status", methods=["GET"])
def ml_status():
    """Get status of ML models"""
    try:
        # Check if models are loaded
        models_loaded = len(ml_predictor.models) > 0

        model_info = {
            "models_loaded": models_loaded,
            "available_models": (
                list(ml_predictor.models.keys()) if models_loaded else []
            ),
            "model_count": len(ml_predictor.models),
            "ready_for_prediction": models_loaded,
        }

        if not models_loaded:
            model_info["message"] = (
                "Models not trained yet. Use /train-models endpoint to train them."
            )

        return response_handler.success(model_info)

    except Exception as e:
        return response_handler.error(f"ML status check failed: {str(e)}", 500)


if __name__ == "__main__":
    # Try to load existing models on startup
    try:
        ml_predictor.load_models()
        print("✅ Pre-trained models loaded successfully")
    except:
        print("⚠️ No pre-trained models found. Use /train-models to train them.")

    app.run(debug=True, host="0.0.0.0", port=5000)
