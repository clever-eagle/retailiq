"""
Machine Learning Predictor for New CSV Uploads
Uses pre-trained models to instantly analyze new retail data
"""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")


class RetailMLPredictor:
    """
    ML Predictor that uses pre-trained models to analyze new CSV data
    """

    def __init__(self, model_dir="trained_models"):
        self.model_dir = model_dir
        self.models = {}
        self.encoders = {}
        self.scalers = {}
        self.feature_importance = {}

        # Load pre-trained models
        self.load_models()

    def load_models(self):
        """
        Load pre-trained models from disk
        """
        try:
            models_file = os.path.join(self.model_dir, "retail_models.pkl")
            with open(models_file, "rb") as f:
                self.models = pickle.load(f)

            encoders_file = os.path.join(self.model_dir, "encoders.pkl")
            with open(encoders_file, "rb") as f:
                self.encoders = pickle.load(f)

            scalers_file = os.path.join(self.model_dir, "scalers.pkl")
            with open(scalers_file, "rb") as f:
                self.scalers = pickle.load(f)

            importance_file = os.path.join(self.model_dir, "feature_importance.pkl")
            with open(importance_file, "rb") as f:
                self.feature_importance = pickle.load(f)

            print(f"✅ Pre-trained models loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to load models: {e}")
            return False

    def analyze_new_data(self, df):
        """
        Analyze new CSV data using pre-trained models
        Returns comprehensive insights for dashboard
        """
        print("🔍 Analyzing new data with pre-trained models...")

        # Validate and clean data
        df = self._validate_data(df)

        results = {
            "data_summary": self._get_data_summary(df),
            "predictions": {},
            "insights": {},
            "recommendations": {},
            "analysis_timestamp": datetime.now().isoformat(),
        }

        # Run all predictions
        try:
            results["predictions"]["customer_segments"] = (
                self._predict_customer_segments(df)
            )
        except Exception as e:
            print(f"⚠️ Customer segmentation failed: {e}")

        try:
            results["predictions"]["sales_forecast"] = self._predict_sales(df)
        except Exception as e:
            print(f"⚠️ Sales prediction failed: {e}")

        try:
            results["predictions"]["churn_risk"] = self._predict_churn(df)
        except Exception as e:
            print(f"⚠️ Churn prediction failed: {e}")

        try:
            results["recommendations"]["products"] = self._get_product_recommendations(
                df
            )
        except Exception as e:
            print(f"⚠️ Product recommendations failed: {e}")

        # Generate insights
        results["insights"] = self._generate_insights(df, results["predictions"])

        return results

    def _validate_data(self, df):
        """
        Validate and clean the uploaded data
        """
        # Required columns
        required_cols = ["transaction_id", "customer_id", "product_name"]

        # Check for required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Clean data
        df = df.copy()

        # Handle missing values
        if (
            "total_amount" not in df.columns
            and "unit_price" in df.columns
            and "quantity" in df.columns
        ):
            df["total_amount"] = df["unit_price"] * df["quantity"]

        if "quantity" not in df.columns:
            df["quantity"] = 1

        if "unit_price" not in df.columns:
            df["unit_price"] = df.get("total_amount", 0) / df["quantity"]

        if "category" not in df.columns:
            df["category"] = df["product_name"].apply(self._categorize_item)

        if "date" not in df.columns:
            df["date"] = datetime.now().strftime("%Y-%m-%d")

        # Convert date
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        return df

    def _get_data_summary(self, df):
        """
        Get basic summary of the new data
        """
        return {
            "total_records": len(df),
            "unique_transactions": df["transaction_id"].nunique(),
            "unique_customers": df["customer_id"].nunique(),
            "unique_products": df["product_name"].nunique(),
            "total_revenue": (
                df["total_amount"].sum() if "total_amount" in df.columns else 0
            ),
            "avg_transaction_value": (
                df.groupby("transaction_id")["total_amount"].sum().mean()
                if "total_amount" in df.columns
                else 0
            ),
            "date_range": {
                "start": df["date"].min().isoformat() if "date" in df.columns else None,
                "end": df["date"].max().isoformat() if "date" in df.columns else None,
            },
            "top_products": df["product_name"].value_counts().head(5).to_dict(),
            "top_categories": (
                df["category"].value_counts().head(5).to_dict()
                if "category" in df.columns
                else {}
            ),
        }

    def _predict_customer_segments(self, df):
        """
        Predict customer segments for new data
        """
        if "customer_segmentation" not in self.models:
            return {"error": "Customer segmentation model not available"}

        # Prepare customer features
        customer_features = (
            df.groupby("customer_id")
            .agg(
                {
                    "total_amount": ["sum", "mean", "count", "std"],
                    "quantity": ["sum", "mean"],
                    "unit_price": ["mean", "max", "min"],
                    "transaction_id": "nunique",
                }
            )
            .reset_index()
        )

        # Flatten column names
        customer_features.columns = [
            "customer_id",
            "total_spent",
            "avg_transaction",
            "purchase_frequency",
            "spending_std",
            "total_items",
            "avg_items",
            "avg_price",
            "max_price",
            "min_price",
            "unique_transactions",
        ]

        # Add derived features
        customer_features["spending_consistency"] = (
            customer_features["spending_std"] / customer_features["avg_transaction"]
        )
        customer_features["price_sensitivity"] = (
            customer_features["max_price"] / customer_features["avg_price"]
        )
        customer_features["items_per_transaction"] = (
            customer_features["total_items"] / customer_features["unique_transactions"]
        )

        # Handle missing/infinite values
        customer_features = customer_features.fillna(0).replace([np.inf, -np.inf], 0)

        # Select features for clustering
        clustering_features = [
            "total_spent",
            "avg_transaction",
            "purchase_frequency",
            "items_per_transaction",
            "price_sensitivity",
        ]

        X = customer_features[clustering_features]

        # Scale features
        scaler = self.scalers.get("customer_segmentation")
        if scaler:
            X_scaled = scaler.transform(X)
        else:
            X_scaled = X

        # Predict segments
        segments = self.models["customer_segmentation"].predict(X_scaled)

        # Map to segment names
        segment_names = {
            0: "Budget Conscious",
            1: "High Value",
            2: "Frequent Shoppers",
            3: "Occasional Buyers",
            4: "Premium Customers",
        }

        customer_features["segment"] = segments
        customer_features["segment_name"] = customer_features["segment"].map(
            segment_names
        )

        # Summary
        segment_summary = customer_features["segment_name"].value_counts().to_dict()

        return {
            "customer_segments": customer_features[
                ["customer_id", "segment_name", "total_spent", "avg_transaction"]
            ].to_dict("records"),
            "segment_distribution": segment_summary,
            "insights": {
                "dominant_segment": max(segment_summary.items(), key=lambda x: x[1])[0],
                "total_customers_analyzed": len(customer_features),
            },
        }

    def _predict_sales(self, df):
        """
        Predict future sales using the trained model
        """
        if "sales_prediction" not in self.models:
            return {"error": "Sales prediction model not available"}

        try:
            # Create time-based features
            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.month
            df["day_of_week"] = df["date"].dt.dayofweek
            df["quarter"] = df["date"].dt.quarter

            # Aggregate daily sales
            daily_sales = (
                df.groupby(["date", "category"])
                .agg(
                    {
                        "total_amount": "sum",
                        "quantity": "sum",
                        "transaction_id": "nunique",
                    }
                )
                .reset_index()
            )

            # Add time features
            daily_sales["month"] = daily_sales["date"].dt.month
            daily_sales["day_of_week"] = daily_sales["date"].dt.dayofweek
            daily_sales["quarter"] = daily_sales["date"].dt.quarter

            # Encode categories
            category_encoder = self.encoders.get("category")
            if category_encoder:
                # Handle new categories
                known_categories = set(category_encoder.classes_)
                daily_sales["category_clean"] = daily_sales["category"].apply(
                    lambda x: x if x in known_categories else "Other"
                )
                daily_sales["category_encoded"] = category_encoder.transform(
                    daily_sales["category_clean"]
                )
            else:
                daily_sales["category_encoded"] = 0

            # Features for prediction
            feature_cols = [
                "month",
                "day_of_week",
                "quarter",
                "category_encoded",
                "quantity",
                "transaction_id",
            ]
            X = daily_sales[feature_cols]

            # Predict sales
            predicted_sales = self.models["sales_prediction"].predict(X)
            daily_sales["predicted_sales"] = predicted_sales

            # Generate future predictions (next 7 days)
            future_predictions = []
            latest_date = df["date"].max()

            for i in range(1, 8):
                future_date = latest_date + timedelta(days=i)
                for category in df["category"].unique():
                    future_features = [
                        future_date.month,
                        future_date.weekday(),
                        future_date.quarter,
                        (
                            category_encoder.transform([category])[0]
                            if category_encoder
                            and category in category_encoder.classes_
                            else 0
                        ),
                        daily_sales["quantity"].mean(),  # Average quantity
                        daily_sales["transaction_id"].mean(),  # Average transactions
                    ]

                    predicted_amount = self.models["sales_prediction"].predict(
                        [future_features]
                    )[0]

                    future_predictions.append(
                        {
                            "date": future_date.strftime("%Y-%m-%d"),
                            "category": category,
                            "predicted_sales": max(
                                0, predicted_amount
                            ),  # Ensure non-negative
                        }
                    )

            return {
                "historical_predictions": daily_sales[
                    ["date", "category", "total_amount", "predicted_sales"]
                ].to_dict("records"),
                "future_forecast": future_predictions,
                "summary": {
                    "avg_daily_sales": daily_sales["total_amount"].mean(),
                    "predicted_avg_daily_sales": daily_sales["predicted_sales"].mean(),
                    "total_predicted_week": sum(
                        [p["predicted_sales"] for p in future_predictions]
                    ),
                },
            }
        except Exception as e:
            return {"error": f"Sales prediction failed: {str(e)}"}

    def _predict_churn(self, df):
        """
        Predict customer churn risk
        """
        if "churn_prediction" not in self.models:
            return {"error": "Churn prediction model not available"}

        try:
            # Calculate customer statistics
            customer_stats = (
                df.groupby("customer_id")
                .agg(
                    {
                        "total_amount": ["sum", "mean", "count"],
                        "quantity": "sum",
                        "transaction_id": "nunique",
                        "category": "nunique",
                    }
                )
                .reset_index()
            )

            customer_stats.columns = [
                "customer_id",
                "total_spent",
                "avg_order_value",
                "order_count",
                "total_items",
                "unique_transactions",
                "categories_purchased",
            ]

            # Features for churn prediction
            feature_cols = [
                "total_spent",
                "avg_order_value",
                "order_count",
                "total_items",
                "categories_purchased",
            ]
            X = customer_stats[feature_cols].fillna(0)

            # Scale features
            scaler = self.scalers.get("churn_prediction")
            if scaler:
                X_scaled = scaler.transform(X)
            else:
                X_scaled = X

            # Predict churn probability
            churn_probabilities = self.models["churn_prediction"].predict_proba(
                X_scaled
            )[:, 1]
            churn_predictions = self.models["churn_prediction"].predict(X_scaled)

            customer_stats["churn_probability"] = churn_probabilities
            customer_stats["churn_risk"] = churn_predictions
            customer_stats["risk_category"] = customer_stats["churn_probability"].apply(
                lambda x: "High" if x > 0.7 else "Medium" if x > 0.4 else "Low"
            )

            # Summary
            risk_summary = customer_stats["risk_category"].value_counts().to_dict()
            high_risk_customers = customer_stats[
                customer_stats["risk_category"] == "High"
            ]

            return {
                "customer_churn_scores": customer_stats[
                    ["customer_id", "churn_probability", "risk_category", "total_spent"]
                ].to_dict("records"),
                "risk_distribution": risk_summary,
                "high_risk_customers": high_risk_customers[
                    ["customer_id", "total_spent", "churn_probability"]
                ].to_dict("records"),
                "summary": {
                    "total_customers_analyzed": len(customer_stats),
                    "high_risk_count": len(high_risk_customers),
                    "avg_churn_probability": customer_stats["churn_probability"].mean(),
                },
            }
        except Exception as e:
            return {"error": f"Churn prediction failed: {str(e)}"}

    def _get_product_recommendations(self, df):
        """
        Generate product recommendations based on purchase patterns
        """
        if "product_recommendation" not in self.models:
            return {"error": "Product recommendation model not available"}

        try:
            recommendation_model = self.models["product_recommendation"]
            similarity_matrix = recommendation_model["similarity_matrix"]

            # Get top products from new data
            top_products = df["product_name"].value_counts().head(10).index.tolist()

            recommendations = []

            for product in top_products:
                if product in similarity_matrix.index:
                    # Get similar products
                    similar_products = similarity_matrix[product].sort_values(
                        ascending=False
                    )[
                        1:6
                    ]  # Top 5 similar

                    for similar_product, similarity_score in similar_products.items():
                        if similarity_score > 0.1:  # Minimum similarity threshold
                            recommendations.append(
                                {
                                    "base_product": product,
                                    "recommended_product": similar_product,
                                    "similarity_score": similarity_score,
                                    "recommendation_strength": (
                                        "High"
                                        if similarity_score > 0.5
                                        else (
                                            "Medium"
                                            if similarity_score > 0.3
                                            else "Low"
                                        )
                                    ),
                                }
                            )

            # Cross-sell opportunities
            cross_sell = (
                df.groupby("transaction_id")["product_name"].apply(list).tolist()
            )
            frequent_combinations = {}

            for transaction in cross_sell:
                if len(transaction) > 1:
                    for i, product1 in enumerate(transaction):
                        for product2 in transaction[i + 1 :]:
                            pair = tuple(sorted([product1, product2]))
                            frequent_combinations[pair] = (
                                frequent_combinations.get(pair, 0) + 1
                            )

            top_combinations = sorted(
                frequent_combinations.items(), key=lambda x: x[1], reverse=True
            )[:10]

            return {
                "product_recommendations": recommendations[
                    :20
                ],  # Top 20 recommendations
                "cross_sell_opportunities": [
                    {
                        "product_pair": list(pair),
                        "frequency": count,
                        "recommendation_type": "Cross-sell",
                    }
                    for pair, count in top_combinations
                ],
                "summary": {
                    "total_recommendations": len(recommendations),
                    "products_analyzed": len(top_products),
                },
            }
        except Exception as e:
            return {"error": f"Product recommendations failed: {str(e)}"}

    def _generate_insights(self, df, predictions):
        """
        Generate business insights from the analysis
        """
        insights = []

        # Revenue insights
        total_revenue = df["total_amount"].sum()
        avg_transaction = df.groupby("transaction_id")["total_amount"].sum().mean()

        insights.append(
            {
                "type": "revenue",
                "title": "Revenue Analysis",
                "description": f"Total revenue: ${total_revenue:,.2f} with average transaction value of ${avg_transaction:.2f}",
                "impact": (
                    "High"
                    if total_revenue > 10000
                    else "Medium" if total_revenue > 1000 else "Low"
                ),
            }
        )

        # Customer insights
        if "customer_segments" in predictions:
            segments = predictions["customer_segments"]
            if "segment_distribution" in segments:
                dominant_segment = max(
                    segments["segment_distribution"].items(), key=lambda x: x[1]
                )[0]
                insights.append(
                    {
                        "type": "customer",
                        "title": "Customer Segmentation",
                        "description": f"Dominant customer segment: {dominant_segment}",
                        "impact": "High",
                    }
                )

        # Churn insights
        if "churn_risk" in predictions and "summary" in predictions["churn_risk"]:
            churn_summary = predictions["churn_risk"]["summary"]
            high_risk_pct = (
                churn_summary.get("high_risk_count", 0)
                / churn_summary.get("total_customers_analyzed", 1)
            ) * 100

            insights.append(
                {
                    "type": "churn",
                    "title": "Churn Risk Analysis",
                    "description": f"{high_risk_pct:.1f}% of customers are at high risk of churning",
                    "impact": (
                        "High"
                        if high_risk_pct > 20
                        else "Medium" if high_risk_pct > 10 else "Low"
                    ),
                }
            )

        # Product insights
        top_category = (
            df["category"].value_counts().index[0] if len(df) > 0 else "Unknown"
        )
        insights.append(
            {
                "type": "product",
                "title": "Product Performance",
                "description": f"Top performing category: {top_category}",
                "impact": "Medium",
            }
        )

        return insights

    def _categorize_item(self, item_name):
        """
        Categorize item based on name
        """
        item_lower = item_name.lower()

        categories = {
            "Electronics": [
                "iphone",
                "samsung",
                "laptop",
                "macbook",
                "ipad",
                "watch",
                "headphones",
                "phone",
                "computer",
            ],
            "Clothing": [
                "shirt",
                "jeans",
                "hoodie",
                "jacket",
                "dress",
                "sweater",
                "pants",
                "shoes",
            ],
            "Sports": [
                "nike",
                "adidas",
                "fitness",
                "gym",
                "sports",
                "running",
                "basketball",
            ],
            "Food & Beverages": [
                "coffee",
                "tea",
                "milk",
                "bread",
                "cheese",
                "juice",
                "water",
            ],
            "Health & Beauty": [
                "vitamin",
                "protein",
                "supplement",
                "shampoo",
                "soap",
                "cream",
            ],
            "Home & Garden": ["kitchen", "furniture", "garden", "tools", "appliance"],
        }

        for category, keywords in categories.items():
            if any(keyword in item_lower for keyword in keywords):
                return category

        return "Other"


if __name__ == "__main__":
    # Test the predictor
    predictor = RetailMLPredictor()

    # Test with sample data
    sample_data = pd.DataFrame(
        {
            "transaction_id": ["T1", "T1", "T2"],
            "customer_id": ["C1", "C1", "C2"],
            "product_name": ["iPhone 15", "AirPods", "Samsung Galaxy"],
            "quantity": [1, 1, 1],
            "unit_price": [999, 199, 799],
            "total_amount": [999, 199, 799],
        }
    )

    results = predictor.analyze_new_data(sample_data)
    print("🎯 Analysis Results:")
    print(f"Data Summary: {results['data_summary']}")
    print(f"Predictions: {list(results['predictions'].keys())}")
    print(f"Insights: {len(results['insights'])} generated")
