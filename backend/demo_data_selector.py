"""
Demo Data Selector - Easy switching between different demo datasets
"""

import os
import pandas as pd


class DemoDataSelector:
    """
    Utility to easily switch between different demo datasets
    """

    def __init__(self, backend_path=None):
        if backend_path is None:
            backend_path = os.path.dirname(__file__)
        self.backend_path = backend_path

        self.available_datasets = {
            "electronics": "demo_data_electronics.csv",
            "food": "demo_data_food.csv",
            "sports": "demo_data_sports.csv",
            "home": "demo_data_home.csv",
            "sample": "sample_market_basket_data.csv",
        }

    def list_datasets(self):
        """List all available demo datasets"""
        print("\nAvailable Demo Datasets:")
        print("=" * 40)
        for key, filename in self.available_datasets.items():
            filepath = os.path.join(self.backend_path, filename)
            if os.path.exists(filepath):
                df = pd.read_csv(filepath)
                print(f"{key.upper()}: {filename}")
                print(f"  - {len(df)} records")
                print(f"  - {df['transaction_id'].nunique()} transactions")
                print(f"  - {df['product_name'].nunique()} unique products")
                if "category" in df.columns:
                    print(f"  - Categories: {', '.join(df['category'].unique())}")
                print()
            else:
                print(f"{key.upper()}: {filename} (NOT FOUND)")
                print()

    def get_dataset_info(self, dataset_name):
        """Get detailed information about a specific dataset"""
        if dataset_name not in self.available_datasets:
            print(
                f"Dataset '{dataset_name}' not found. Available: {list(self.available_datasets.keys())}"
            )
            return None

        filename = self.available_datasets[dataset_name]
        filepath = os.path.join(self.backend_path, filename)

        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return None

        df = pd.read_csv(filepath)

        info = {
            "name": dataset_name,
            "filename": filename,
            "total_records": len(df),
            "unique_transactions": df["transaction_id"].nunique(),
            "unique_products": df["product_name"].nunique(),
            "unique_customers": df["customer_id"].nunique(),
            "date_range": {"start": df["date"].min(), "end": df["date"].max()},
            "total_revenue": df["total_amount"].sum(),
            "avg_transaction_value": df.groupby("transaction_id")["total_amount"]
            .sum()
            .mean(),
        }

        if "category" in df.columns:
            info["categories"] = df["category"].unique().tolist()
            info["category_breakdown"] = df["category"].value_counts().to_dict()

        if "customer_segment" in df.columns:
            info["customer_segments"] = df["customer_segment"].unique().tolist()
            info["segment_breakdown"] = df["customer_segment"].value_counts().to_dict()

        return info

    def load_dataset(self, dataset_name):
        """Load a specific dataset"""
        if dataset_name not in self.available_datasets:
            raise ValueError(
                f"Dataset '{dataset_name}' not found. Available: {list(self.available_datasets.keys())}"
            )

        filename = self.available_datasets[dataset_name]
        filepath = os.path.join(self.backend_path, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        return pd.read_csv(filepath)

    def switch_default_dataset(self, dataset_name):
        """
        Switch the default dataset by copying it to sample_market_basket_data.csv
        """
        if dataset_name not in self.available_datasets:
            raise ValueError(
                f"Dataset '{dataset_name}' not found. Available: {list(self.available_datasets.keys())}"
            )

        source_file = os.path.join(
            self.backend_path, self.available_datasets[dataset_name]
        )
        target_file = os.path.join(self.backend_path, "sample_market_basket_data.csv")

        if not os.path.exists(source_file):
            raise FileNotFoundError(f"Source file not found: {source_file}")

        # Copy the dataset
        df = pd.read_csv(source_file)
        df.to_csv(target_file, index=False)

        print(f"✅ Default dataset switched to: {dataset_name}")
        print(f"📁 File: {self.available_datasets[dataset_name]}")
        print(f"📊 Records: {len(df)}")
        print(f"🛒 Transactions: {df['transaction_id'].nunique()}")

        return True


if __name__ == "__main__":
    # Demo usage
    selector = DemoDataSelector()

    print("🔍 DEMO DATA SELECTOR")
    print("=" * 50)

    # List all datasets
    selector.list_datasets()

    # Get info about electronics dataset
    print("📱 ELECTRONICS DATASET INFO:")
    print("-" * 30)
    info = selector.get_dataset_info("electronics")
    if info:
        print(f"Total Revenue: ${info['total_revenue']:,.2f}")
        print(f"Avg Transaction: ${info['avg_transaction_value']:.2f}")
        print(f"Categories: {', '.join(info['categories'])}")
        print(f"Customer Segments: {', '.join(info['customer_segments'])}")

    print("\n" + "=" * 50)
    print("To switch datasets, use:")
    print("selector.switch_default_dataset('electronics')")
    print("selector.switch_default_dataset('food')")
    print("selector.switch_default_dataset('sports')")
    print("selector.switch_default_dataset('home')")
