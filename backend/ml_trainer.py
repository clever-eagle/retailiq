"""
Machine Learning Model Trainer for Retail Analytics
Trains models on existing data and saves them for instant predictions on new uploads
"""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.cluster import KMeans
import joblib
import warnings

warnings.filterwarnings("ignore")


class RetailMLTrainer:
    """
    ML Trainer for retail analytics - trains multiple models for different predictions
    """

    def __init__(self, model_dir="trained_models"):
        self.model_dir = model_dir
        self.models = {}
        self.encoders = {}
        self.scalers = {}
        self.feature_importance = {}

        # Create model directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)

    def prepare_features(self, df):
        """
        Extract features from transaction data for ML training
        """
        print("🔧 Preparing features for ML training...")

        # Create aggregated features by customer
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

        # Add customer behavior features
        customer_features["spending_consistency"] = (
            customer_features["spending_std"] / customer_features["avg_transaction"]
        )
        customer_features["price_sensitivity"] = (
            customer_features["max_price"] / customer_features["avg_price"]
        )
        customer_features["items_per_transaction"] = (
            customer_features["total_items"] / customer_features["unique_transactions"]
        )

        # Product features
        product_features = (
            df.groupby("product_name")
            .agg(
                {
                    "total_amount": ["sum", "mean", "count"],
                    "quantity": "sum",
                    "customer_id": "nunique",
                }
            )
            .reset_index()
        )

        product_features.columns = [
            "product_name",
            "product_revenue",
            "avg_product_value",
            "product_popularity",
            "total_quantity_sold",
            "unique_customers",
        ]

        # Category insights
        category_features = (
            df.groupby("category")
            .agg(
                {
                    "total_amount": ["sum", "mean"],
                    "customer_id": "nunique",
                    "transaction_id": "nunique",
                }
            )
            .reset_index()
        )

        category_features.columns = [
            "category",
            "category_revenue",
            "avg_category_value",
            "category_customers",
            "category_transactions",
        ]

        return customer_features, product_features, category_features

    def train_customer_segmentation_model(self, customer_features):
        """
        Train customer segmentation model using K-Means clustering
        """
        print("🎯 Training Customer Segmentation Model...")

        # Select features for clustering
        clustering_features = [
            "total_spent",
            "avg_transaction",
            "purchase_frequency",
            "items_per_transaction",
            "price_sensitivity",
        ]

        # Handle missing values
        X_cluster = customer_features[clustering_features].fillna(0)

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_cluster)

        # Train K-Means with 5 segments
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        # Add cluster labels
        customer_features["segment"] = clusters

        # Define segment names based on characteristics
        segment_names = {
            0: "Budget Conscious",
            1: "High Value",
            2: "Frequent Shoppers",
            3: "Occasional Buyers",
            4: "Premium Customers",
        }

        customer_features["segment_name"] = customer_features["segment"].map(
            segment_names
        )

        # Save model and scaler
        self.models["customer_segmentation"] = kmeans
        self.scalers["customer_segmentation"] = scaler

        print(
            f"✅ Customer Segmentation trained with {len(clustering_features)} features"
        )
        print(f"📊 Segments distribution:")
        for segment, name in segment_names.items():
            count = sum(clusters == segment)
            print(f"   {name}: {count} customers ({count/len(clusters)*100:.1f}%)")

        return customer_features

    def train_sales_prediction_model(self, df):
        """
        Train sales prediction model (Random Forest Regressor)
        """
        print("📈 Training Sales Prediction Model...")

        # Create time-based features
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.month
        df["day_of_week"] = df["date"].dt.dayofweek
        df["quarter"] = df["date"].dt.quarter

        # Aggregate daily sales
        daily_sales = (
            df.groupby(["date", "category"])
            .agg(
                {"total_amount": "sum", "quantity": "sum", "transaction_id": "nunique"}
            )
            .reset_index()
        )

        # Add time features
        daily_sales["month"] = daily_sales["date"].dt.month
        daily_sales["day_of_week"] = daily_sales["date"].dt.dayofweek
        daily_sales["quarter"] = daily_sales["date"].dt.quarter

        # Encode category
        le_category = LabelEncoder()
        daily_sales["category_encoded"] = le_category.fit_transform(
            daily_sales["category"]
        )

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
        y = daily_sales["total_amount"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train Random Forest
        rf_sales = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_sales.fit(X_train, y_train)

        # Evaluate
        y_pred = rf_sales.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        # Save model and encoder
        self.models["sales_prediction"] = rf_sales
        self.encoders["category"] = le_category
        self.feature_importance["sales_prediction"] = dict(
            zip(feature_cols, rf_sales.feature_importances_)
        )

        print(f"✅ Sales Prediction Model trained with RMSE: ${rmse:.2f}")
        print("📊 Feature Importance:")
        for feature, importance in self.feature_importance["sales_prediction"].items():
            print(f"   {feature}: {importance:.3f}")

        return rf_sales

    def train_product_recommendation_model(self, df):
        """
        Train product recommendation model using association rules
        """
        print("🛒 Training Product Recommendation Model...")

        # Create customer-product matrix
        customer_product = (
            df.groupby(["customer_id", "product_name"])["quantity"]
            .sum()
            .unstack(fill_value=0)
        )

        # Binary matrix (bought/not bought)
        customer_product_binary = (customer_product > 0).astype(int)

        # Calculate product similarity (cosine similarity)
        from sklearn.metrics.pairwise import cosine_similarity

        product_similarity = cosine_similarity(customer_product_binary.T)

        # Create similarity DataFrame
        similarity_df = pd.DataFrame(
            product_similarity,
            index=customer_product_binary.columns,
            columns=customer_product_binary.columns,
        )

        # Save model
        self.models["product_recommendation"] = {
            "similarity_matrix": similarity_df,
            "customer_product_matrix": customer_product_binary,
        }

        print(
            f"✅ Product Recommendation Model trained with {len(customer_product_binary.columns)} products"
        )

        return similarity_df

    def train_churn_prediction_model(self, df):
        """
        Train customer churn prediction model
        """
        print("⚠️ Training Churn Prediction Model...")

        # Calculate days since last purchase for each customer
        df["date"] = pd.to_datetime(df["date"])
        latest_date = df["date"].max()

        customer_last_purchase = df.groupby("customer_id")["date"].max().reset_index()
        customer_last_purchase["days_since_last_purchase"] = (
            latest_date - customer_last_purchase["date"]
        ).dt.days

        # Define churn (> 90 days since last purchase)
        customer_last_purchase["is_churned"] = (
            customer_last_purchase["days_since_last_purchase"] > 90
        ).astype(int)

        # Get customer features
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

        # Merge with churn labels
        churn_data = customer_stats.merge(
            customer_last_purchase[["customer_id", "is_churned"]], on="customer_id"
        )

        # Features for churn prediction
        feature_cols = [
            "total_spent",
            "avg_order_value",
            "order_count",
            "total_items",
            "categories_purchased",
        ]
        X = churn_data[feature_cols].fillna(0)
        y = churn_data["is_churned"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train Random Forest Classifier
        rf_churn = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_churn.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = rf_churn.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        # Save model and scaler
        self.models["churn_prediction"] = rf_churn
        self.scalers["churn_prediction"] = scaler
        self.feature_importance["churn_prediction"] = dict(
            zip(feature_cols, rf_churn.feature_importances_)
        )

        print(f"✅ Churn Prediction Model trained with accuracy: {accuracy:.3f}")
        print("📊 Feature Importance:")
        for feature, importance in self.feature_importance["churn_prediction"].items():
            print(f"   {feature}: {importance:.3f}")

        return rf_churn

    def train_all_models(self, data_file=None):
        """
        Train all ML models on the existing dataset
        """
        print("🚀 Starting ML Model Training Pipeline...")
        print("=" * 60)

        # Load data
        if data_file is None:
            # Try multiple data sources
            data_sources = [
                "large_market_basket_data.csv",
                "demo_data_electronics.csv",
                "demo_data_sports.csv",
                "demo_data_food.csv",
            ]

            df = None
            for source in data_sources:
                file_path = os.path.join(os.path.dirname(__file__), source)
                if os.path.exists(file_path):
                    print(f"📁 Loading training data from: {source}")
                    if source == "large_market_basket_data.csv":
                        # Handle the special format of large dataset
                        raw_df = pd.read_csv(file_path)
                        df = self._process_large_dataset(raw_df)
                    else:
                        df = pd.read_csv(file_path)
                    break

            if df is None:
                raise FileNotFoundError("No training data found!")
        else:
            df = pd.read_csv(data_file)

        print(
            f"📊 Training data loaded: {len(df)} records, {df['transaction_id'].nunique()} transactions"
        )

        # Prepare features
        customer_features, product_features, category_features = self.prepare_features(
            df
        )

        # Train all models
        models_trained = []

        try:
            # 1. Customer Segmentation
            customer_features = self.train_customer_segmentation_model(
                customer_features
            )
            models_trained.append("Customer Segmentation")
        except Exception as e:
            print(f"❌ Failed to train Customer Segmentation: {e}")

        try:
            # 2. Sales Prediction
            self.train_sales_prediction_model(df)
            models_trained.append("Sales Prediction")
        except Exception as e:
            print(f"❌ Failed to train Sales Prediction: {e}")

        try:
            # 3. Product Recommendation
            self.train_product_recommendation_model(df)
            models_trained.append("Product Recommendation")
        except Exception as e:
            print(f"❌ Failed to train Product Recommendation: {e}")

        try:
            # 4. Churn Prediction
            self.train_churn_prediction_model(df)
            models_trained.append("Churn Prediction")
        except Exception as e:
            print(f"❌ Failed to train Churn Prediction: {e}")

        # Save all models
        self.save_models()

        print("=" * 60)
        print(f"🎉 Training Complete! Models trained: {len(models_trained)}")
        for model in models_trained:
            print(f"   ✅ {model}")

        return {
            "models_trained": models_trained,
            "training_data_size": len(df),
            "unique_transactions": df["transaction_id"].nunique(),
            "unique_customers": df["customer_id"].nunique(),
            "unique_products": df["product_name"].nunique(),
            "training_timestamp": datetime.now().isoformat(),
        }

    def _process_large_dataset(self, df):
        """
        Process the large market basket dataset format
        """
        processed_rows = []

        for _, row in df.iterrows():
            transaction_id = row["transaction_id"]
            customer_id = row["customer_id"]
            date = row["date"]

            # Split items by semicolon
            items = row["items"].split(";")

            for item in items:
                processed_rows.append(
                    {
                        "transaction_id": transaction_id,
                        "customer_id": customer_id,
                        "product_name": item.strip(),
                        "date": date,
                        "quantity": 1,
                        "unit_price": self._estimate_price(item.strip()),
                        "category": self._categorize_item(item.strip()),
                    }
                )

        processed_df = pd.DataFrame(processed_rows)
        processed_df["total_amount"] = (
            processed_df["unit_price"] * processed_df["quantity"]
        )

        return processed_df

    def _estimate_price(self, item_name):
        """Estimate price based on item name"""
        item_lower = item_name.lower()

        if any(word in item_lower for word in ["iphone", "macbook", "laptop"]):
            return np.random.uniform(800, 1500)
        elif any(word in item_lower for word in ["nike", "adidas", "shoes"]):
            return np.random.uniform(60, 200)
        elif any(word in item_lower for word in ["coffee", "tea", "food"]):
            return np.random.uniform(5, 25)
        else:
            return np.random.uniform(10, 100)

    def _categorize_item(self, item_name):
        """Categorize item based on name"""
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
            ],
            "Clothing": ["shirt", "jeans", "hoodie", "jacket", "dress", "sweater"],
            "Sports": ["nike", "adidas", "fitness", "gym", "sports"],
            "Food": ["coffee", "tea", "milk", "bread", "cheese"],
            "Health": ["vitamin", "protein", "supplement", "shampoo", "soap"],
        }

        for category, keywords in categories.items():
            if any(keyword in item_lower for keyword in keywords):
                return category

        return "Other"

    def save_models(self):
        """
        Save all trained models to disk
        """
        print("💾 Saving trained models...")

        # Save models
        models_file = os.path.join(self.model_dir, "retail_models.pkl")
        with open(models_file, "wb") as f:
            pickle.dump(self.models, f)

        # Save encoders
        encoders_file = os.path.join(self.model_dir, "encoders.pkl")
        with open(encoders_file, "wb") as f:
            pickle.dump(self.encoders, f)

        # Save scalers
        scalers_file = os.path.join(self.model_dir, "scalers.pkl")
        with open(scalers_file, "wb") as f:
            pickle.dump(self.scalers, f)

        # Save feature importance
        importance_file = os.path.join(self.model_dir, "feature_importance.pkl")
        with open(importance_file, "wb") as f:
            pickle.dump(self.feature_importance, f)

        print(f"✅ Models saved to {self.model_dir}/")

    def load_models(self):
        """
        Load trained models from disk
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

            print(f"✅ Models loaded from {self.model_dir}/")
            return True
        except Exception as e:
            print(f"❌ Failed to load models: {e}")
            return False


if __name__ == "__main__":
    # Train all models
    trainer = RetailMLTrainer()
    training_results = trainer.train_all_models()

    print("\n🎯 Training Summary:")
    print(f"Models trained: {training_results['models_trained']}")
    print(f"Training data: {training_results['training_data_size']} records")
    print(f"Customers: {training_results['unique_customers']}")
    print(f"Products: {training_results['unique_products']}")
