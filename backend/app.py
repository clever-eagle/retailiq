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

app = Flask(__name__)
CORS(app)

# Initialize models
apriori_analyzer = AprioriMarketBasket()
sales_forecaster = SalesForecaster()
data_processor = DataProcessor()
response_handler = ResponseHandler()


# Store for uploaded data and analysis - starts empty
class DataStore:
    def __init__(self):
        self.uploaded_data = None
        self.current_analysis = None

    def set_data(self, data, analysis):
        self.uploaded_data = data
        self.current_analysis = analysis
        print(f"🔄 DataStore: Stored {len(data)} records")

    def get_data(self):
        print(f"🔍 DataStore: Has data: {self.uploaded_data is not None}")
        if self.uploaded_data is not None:
            print(f"📊 DataStore: Records: {len(self.uploaded_data)}")
        return self.uploaded_data, self.current_analysis

    def has_data(self):
        return self.uploaded_data is not None and len(self.uploaded_data) > 0

    def clear_data(self):
        """Reset all data to empty state"""
        self.uploaded_data = None
        self.current_analysis = None
        print("🗑️ DataStore: All data cleared")


# Global data store
data_store = DataStore()


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/reset-data", methods=["POST"])
def reset_data():
    """Reset all uploaded data and analysis - brings system back to empty state"""
    try:
        data_store.clear_data()

        return response_handler.success(
            {
                "message": "All data has been reset successfully",
                "status": "cleared",
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return response_handler.error(f"Reset failed: {str(e)}", 500)


@app.route("/upload-data", methods=["POST"])
def upload_data():
    """Upload CSV data and get comprehensive analysis - ONLY analyzes your uploaded data"""
    try:
        if "file" not in request.files:
            return response_handler.error("No file provided", 400)

        file = request.files["file"]
        if file.filename == "":
            return response_handler.error("No file selected", 400)

        if not file.filename.endswith(".csv"):
            return response_handler.error("File must be a CSV", 400)

        print(f"📁 Processing uploaded file: {file.filename}")

        # Process ONLY the uploaded file - no default data
        df = pd.read_csv(file)

        # Check if this is market basket format (has 'items' column) or standard format
        if "items" in df.columns:
            print("🛒 Detected market basket format - processing...")
            processed_data = data_processor.process_large_market_basket_data(df)
        else:
            print("📊 Detected standard format - processing...")
            processed_data = data_processor.validate_and_clean_data(df)

        print(f"✅ Processing {len(processed_data)} records from your CSV...")

        # Get comprehensive analysis of YOUR data
        data_summary = data_processor.get_data_summary(processed_data)

        # Store the analysis
        analysis = {
            "file_info": {
                "filename": file.filename,
                "upload_timestamp": datetime.now().isoformat(),
                "records": len(processed_data),
                "columns": list(processed_data.columns),
                "format_detected": (
                    "market_basket" if "items" in df.columns else "standard"
                ),
            },
            "analysis": data_summary,
            "status": "completed",
        }

        # Store in data store
        data_store.set_data(processed_data, analysis)

        return response_handler.success(
            {
                "message": f"Successfully analyzed your CSV: {file.filename}",
                "file_info": analysis["file_info"],
                "analysis": data_summary,
            }
        )

    except Exception as e:
        return response_handler.error(f"Analysis failed: {str(e)}", 500)


@app.route("/data-summary", methods=["GET"])
def data_summary():
    """Get summary of YOUR uploaded data only - returns empty if no CSV uploaded"""
    try:
        uploaded_data, current_analysis = data_store.get_data()

        if not data_store.has_data():
            return response_handler.success(
                {
                    "message": "No data uploaded yet",
                    "has_data": False,
                    "instruction": "Upload a CSV file to see analysis",
                }
            )

        # Return analysis of YOUR uploaded data
        summary = data_processor.get_data_summary(uploaded_data)

        return response_handler.success(
            {
                "message": "Analysis of your uploaded data",
                "has_data": True,
                "file_info": (
                    current_analysis["file_info"] if current_analysis else None
                ),
                "analysis": summary,
            }
        )

    except Exception as e:
        return response_handler.error(f"Data summary failed: {str(e)}", 500)


@app.route("/current-analysis", methods=["GET"])
def get_current_analysis():
    """Get analysis of currently uploaded CSV - empty if no CSV uploaded"""
    try:
        uploaded_data, current_analysis = data_store.get_data()

        if current_analysis is None:
            return response_handler.success(
                {
                    "message": "No CSV analyzed yet",
                    "has_analysis": False,
                    "instruction": "Upload a CSV file using /upload-data to see analysis",
                }
            )

        return response_handler.success(
            {
                "message": "Current CSV analysis",
                "has_analysis": True,
                "analysis": current_analysis,
                "last_updated": current_analysis.get("file_info", {}).get(
                    "upload_timestamp", "Unknown"
                ),
            }
        )

    except Exception as e:
        return response_handler.error(f"Failed to retrieve analysis: {str(e)}", 500)


@app.route("/sales-forecast", methods=["POST"])
def sales_forecast():
    """Generate sales forecast based on uploaded data"""
    try:
        uploaded_data, current_analysis = data_store.get_data()

        if not data_store.has_data():
            return response_handler.error(
                "No data available for forecasting. Please upload a CSV file first.",
                400,
            )

        # Get request parameters
        data = request.get_json() or {}
        forecast_days = data.get("forecast_days", 30)

        # Simple forecast based on current data
        df = uploaded_data

        # Calculate daily averages
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            daily_sales = df.groupby("date")["total_amount"].sum().mean()
        else:
            daily_sales = df["total_amount"].sum() / 30  # Assume 30 days if no date

        # Generate simple forecast (could be enhanced with ML later)
        forecast_data = []
        base_date = datetime.now()

        for i in range(forecast_days):
            forecast_date = base_date + timedelta(days=i + 1)
            # Add some variation (±15%)
            variation = 0.85 + (0.3 * (i % 7) / 7)  # Weekly pattern
            predicted_sales = daily_sales * variation

            forecast_data.append(
                {
                    "date": forecast_date.strftime("%Y-%m-%d"),
                    "predicted_sales": round(predicted_sales, 2),
                    "confidence": 0.75 - (i * 0.01),  # Decreasing confidence over time
                }
            )

        # Calculate summary metrics
        total_forecast = sum(item["predicted_sales"] for item in forecast_data)
        avg_daily_forecast = total_forecast / forecast_days

        return response_handler.success(
            {
                "forecast": forecast_data,
                "summary": {
                    "total_forecast": round(total_forecast, 2),
                    "avg_daily_forecast": round(avg_daily_forecast, 2),
                    "forecast_period": f"{forecast_days} days",
                    "confidence_score": 0.75,
                    "based_on_records": len(uploaded_data),
                },
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "method": "moving_average",
                    "data_source": (
                        current_analysis["file_info"]["filename"]
                        if current_analysis
                        else "uploaded_data"
                    ),
                },
            }
        )

    except Exception as e:
        return response_handler.error(f"Sales forecast failed: {str(e)}", 500)


@app.route("/market-basket-analysis", methods=["POST"])
def market_basket_analysis():
    """Perform market basket analysis on uploaded data"""
    try:
        uploaded_data, current_analysis = data_store.get_data()

        if not data_store.has_data():
            return response_handler.error(
                "No data available for market basket analysis. Please upload a CSV file first.",
                400,
            )

        # Get request parameters
        data = request.get_json() or {}
        min_support = data.get("min_support", 0.01)
        min_confidence = data.get("min_confidence", 0.2)

        # Use the existing apriori analyzer
        result = apriori_analyzer.analyze(uploaded_data, min_support, min_confidence)

        return response_handler.success(
            {
                "analysis": result,
                "parameters": {
                    "min_support": min_support,
                    "min_confidence": min_confidence,
                },
                "data_info": {
                    "total_transactions": (
                        len(uploaded_data["transaction_id"].unique())
                        if "transaction_id" in uploaded_data.columns
                        else len(uploaded_data)
                    ),
                    "total_products": (
                        len(uploaded_data["product_name"].unique())
                        if "product_name" in uploaded_data.columns
                        else 0
                    ),
                },
            }
        )

    except Exception as e:
        return response_handler.error(f"Market basket analysis failed: {str(e)}", 500)


@app.route("/get-recommendations", methods=["POST"])
def get_recommendations():
    """Get product recommendations based on uploaded data"""
    try:
        uploaded_data, current_analysis = data_store.get_data()

        if not data_store.has_data():
            return response_handler.error(
                "No data available for recommendations. Please upload a CSV file first.",
                400,
            )

        # Get request parameters
        data = request.get_json() or {}
        current_items = data.get("items", [])

        # Simple recommendation based on product co-occurrence
        if (
            "product_name" in uploaded_data.columns
            and "transaction_id" in uploaded_data.columns
        ):
            # Find products that frequently appear together
            transaction_products = uploaded_data.groupby("transaction_id")[
                "product_name"
            ].apply(list)

            recommendations = []
            product_counts = {}

            # Count product co-occurrences
            for products in transaction_products:
                if any(item in products for item in current_items):
                    for product in products:
                        if product not in current_items:
                            product_counts[product] = product_counts.get(product, 0) + 1

            # Sort by frequency and take top 10
            sorted_products = sorted(
                product_counts.items(), key=lambda x: x[1], reverse=True
            )[:10]

            for product, count in sorted_products:
                recommendations.append(
                    {
                        "product": product,
                        "confidence": min(count / len(transaction_products) * 100, 95),
                        "frequency": count,
                        "reason": f"Frequently bought with your selected items",
                    }
                )
        else:
            recommendations = []

        return response_handler.success(
            {
                "recommendations": recommendations,
                "input_items": current_items,
                "total_recommendations": len(recommendations),
            }
        )

    except Exception as e:
        return response_handler.error(f"Recommendations failed: {str(e)}", 500)


@app.route("/sales-trends", methods=["GET"])
def sales_trends():
    """Get sales trends from uploaded data"""
    try:
        uploaded_data, current_analysis = data_store.get_data()

        if not data_store.has_data():
            return response_handler.error(
                "No data available for trends analysis. Please upload a CSV file first.",
                400,
            )

        df = uploaded_data

        # Calculate basic trends
        total_revenue = df["total_amount"].sum() if "total_amount" in df.columns else 0
        total_transactions = (
            len(df["transaction_id"].unique())
            if "transaction_id" in df.columns
            else len(df)
        )

        # Monthly trends (if date available)
        monthly_trends = []
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.to_period("M")
            monthly_data = df.groupby("month")["total_amount"].sum()

            for month, revenue in monthly_data.items():
                monthly_trends.append(
                    {
                        "month": str(month),
                        "revenue": round(revenue, 2),
                        "transactions": len(df[df["month"] == month]),
                    }
                )

        # Category trends
        category_trends = {}
        if "category" in df.columns:
            category_data = df.groupby("category")["total_amount"].sum()
            category_trends = {cat: round(rev, 2) for cat, rev in category_data.items()}

        return response_handler.success(
            {
                "summary": {
                    "total_revenue": round(total_revenue, 2),
                    "total_transactions": total_transactions,
                    "revenue_growth_rate": 0,  # Would need historical data
                    "avg_transaction_value": round(
                        (
                            total_revenue / total_transactions
                            if total_transactions > 0
                            else 0
                        ),
                        2,
                    ),
                },
                "monthly_trends": monthly_trends,
                "category_trends": category_trends,
                "weekly_patterns": {},  # Could be enhanced
                "data_period": {
                    "start": (
                        df["date"].min().isoformat() if "date" in df.columns else None
                    ),
                    "end": (
                        df["date"].max().isoformat() if "date" in df.columns else None
                    ),
                },
            }
        )

    except Exception as e:
        return response_handler.error(f"Sales trends analysis failed: {str(e)}", 500)


if __name__ == "__main__":
    print("🚀 RetailIQ Backend - CSV Analysis System")
    print("📄 Upload a CSV file to get comprehensive analysis")
    print("🌐 Starting server on http://localhost:5000")

    app.run(debug=True, host="0.0.0.0", port=5000)
