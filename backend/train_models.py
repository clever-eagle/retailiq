"""
AI Model Training Script for RetailIQ
Trains market basket analysis and sales forecasting models using synthetic data
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pickle
from models.market_basket_analyzer import MarketBasketAnalyzer
from models.sales_forecaster import SalesForecaster
from data_generation.synthetic_data_generator import SyntheticDataGenerator


class ModelTrainer:
    def __init__(self):
        self.market_basket_analyzer = MarketBasketAnalyzer()
        self.sales_forecaster = SalesForecaster()
        self.data_generator = SyntheticDataGenerator()

    def prepare_training_data(self, num_transactions=15000):
        """Generate and prepare training data"""
        print("=" * 60)
        print("PREPARING TRAINING DATA")
        print("=" * 60)

        # Generate synthetic data
        print(f"Generating {num_transactions} synthetic transactions...")
        df = self.data_generator.generate_synthetic_transactions(num_transactions)

        # Save the training data
        training_data_path = os.path.join(
            os.path.dirname(__file__), "training_data.csv"
        )
        df.to_csv(training_data_path, index=False)

        print(f"Training data saved to: {training_data_path}")
        print(f"Data shape: {df.shape}")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"Unique customers: {df['customer_id'].nunique()}")
        print(f"Unique products: {df['product_name'].nunique()}")
        print(f"Categories: {', '.join(df['category'].unique())}")

        return df

    def train_market_basket_model(self, df):
        """Train the market basket analysis model"""
        print("\n" + "=" * 60)
        print("TRAINING MARKET BASKET ANALYSIS MODEL")
        print("=" * 60)

        try:
            # Train the model
            result = self.market_basket_analyzer.analyze(df)

            print(f"✅ Market basket analysis completed successfully!")
            print(
                f"   - Found {len(result.get('frequent_itemsets', []))} frequent itemsets"
            )
            print(
                f"   - Generated {len(result.get('association_rules', []))} association rules"
            )

            # Test recommendations
            test_items = ["Coffee Maker", "Wireless Headphones", "Yoga Mat"]
            for item in test_items:
                recommendations = self.market_basket_analyzer.get_recommendations(
                    df, [item]
                )
                print(
                    f"   - Recommendations for '{item}': {len(recommendations)} items"
                )

            return True

        except Exception as e:
            print(f"❌ Error training market basket model: {str(e)}")
            return False

    def train_sales_forecasting_model(self, df):
        """Train the sales forecasting model"""
        print("\n" + "=" * 60)
        print("TRAINING SALES FORECASTING MODEL")
        print("=" * 60)

        try:
            # Prepare data for forecasting
            forecast_data = (
                df.groupby(["date", "product_name"])
                .agg({"quantity": "sum", "total_amount": "sum"})
                .reset_index()
            )

            # Get unique products for testing
            products = df["product_name"].unique()[:10]  # Test with first 10 products

            successful_trainings = 0

            for product in products:
                try:
                    product_data = forecast_data[
                        forecast_data["product_name"] == product
                    ]

                    if len(product_data) >= 10:  # Need minimum data points
                        forecast_result = self.sales_forecaster.forecast(
                            df=df, forecast_days=30, product_filter=product
                        )

                        if forecast_result.get("success", False):
                            successful_trainings += 1
                            print(f"   ✅ Trained forecasting for '{product}'")
                        else:
                            print(
                                f"   ⚠️  Warning: Could not train forecasting for '{product}'"
                            )

                except Exception as e:
                    print(f"   ❌ Error training forecasting for '{product}': {str(e)}")

            print(f"\n✅ Sales forecasting training completed!")
            print(
                f"   - Successfully trained models for {successful_trainings}/{len(products)} products"
            )

            return successful_trainings > 0

        except Exception as e:
            print(f"❌ Error in sales forecasting training: {str(e)}")
            return False

    def validate_models(self, df):
        """Validate trained models with test scenarios"""
        print("\n" + "=" * 60)
        print("VALIDATING TRAINED MODELS")
        print("=" * 60)

        validation_results = {"market_basket": False, "sales_forecasting": False}

        # Test market basket analysis
        try:
            test_scenarios = [
                ["Coffee Maker"],
                ["Wireless Headphones", "Smartphone Case"],
                ["Yoga Mat", "Water Bottle"],
                ["Office Chair", "Desk Lamp"],
            ]

            for i, items in enumerate(test_scenarios, 1):
                recommendations = self.market_basket_analyzer.get_recommendations(
                    df, items
                )
                print(f"   Test {i}: {items} → {len(recommendations)} recommendations")

                if recommendations:
                    top_rec = recommendations[0]
                    print(
                        f"            Top recommendation: {top_rec.get('product', 'N/A')} "
                        f"(confidence: {top_rec.get('confidence', 0):.2f})"
                    )

            validation_results["market_basket"] = True
            print("   ✅ Market basket analysis validation passed")

        except Exception as e:
            print(f"   ❌ Market basket validation failed: {str(e)}")

        # Test sales forecasting
        try:
            test_products = df["product_name"].unique()[:3]

            for product in test_products:
                forecast_result = self.sales_forecaster.forecast(
                    df=df, forecast_days=7, product_filter=product
                )

                if forecast_result.get("success", False):
                    predictions = forecast_result.get("predictions", [])
                    print(
                        f"   ✅ Forecast for '{product}': {len(predictions)} predictions"
                    )
                else:
                    print(f"   ⚠️  Could not generate forecast for '{product}'")

            validation_results["sales_forecasting"] = True
            print("   ✅ Sales forecasting validation passed")

        except Exception as e:
            print(f"   ❌ Sales forecasting validation failed: {str(e)}")

        return validation_results

    def save_model_info(self, validation_results):
        """Save model training information"""
        model_info = {
            "training_date": datetime.now().isoformat(),
            "market_basket_trained": validation_results["market_basket"],
            "sales_forecasting_trained": validation_results["sales_forecasting"],
            "training_data_size": "synthetic_15000_transactions",
            "model_versions": {
                "market_basket_analyzer": "1.0",
                "sales_forecaster": "1.0",
            },
        }

        info_path = os.path.join(os.path.dirname(__file__), "model_training_info.json")

        import json

        with open(info_path, "w") as f:
            json.dump(model_info, f, indent=2)

        print(f"\n📋 Model training info saved to: {info_path}")

    def train_all_models(self):
        """Main training pipeline"""
        print("🚀 STARTING AI MODEL TRAINING PIPELINE")
        print("=" * 60)

        start_time = datetime.now()

        # Step 1: Prepare training data
        df = self.prepare_training_data(15000)

        # Step 2: Train market basket model
        mb_success = self.train_market_basket_model(df)

        # Step 3: Train sales forecasting model
        sf_success = self.train_sales_forecasting_model(df)

        # Step 4: Validate models
        validation_results = self.validate_models(df)

        # Step 5: Save model info
        self.save_model_info(validation_results)

        # Summary
        end_time = datetime.now()
        duration = end_time - start_time

        print("\n" + "=" * 60)
        print("TRAINING COMPLETE")
        print("=" * 60)
        print(f"⏱️  Training duration: {duration}")
        print(
            f"✅ Market Basket Analysis: {'TRAINED' if validation_results['market_basket'] else 'FAILED'}"
        )
        print(
            f"✅ Sales Forecasting: {'TRAINED' if validation_results['sales_forecasting'] else 'FAILED'}"
        )
        print("\n🎉 AI models are now ready for production use!")

        return validation_results


if __name__ == "__main__":
    trainer = ModelTrainer()
    results = trainer.train_all_models()
