#!/usr/bin/env python3
"""
Test script for the enhanced ML-powered backend
Tests the new functionality: CSV upload -> model retraining -> recent analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json


def generate_synthetic_transactions():
    """Generate a table of random synthetic transactions for demo and testing purposes."""

    # Sample data similar to your existing format
    products = [
        "iPhone 15",
        "MacBook Pro",
        "AirPods Pro",
        "Nike Shoes",
        "Protein Bars",
        "Coffee",
        "Bread",
        "Milk",
        "Shampoo",
        "T-Shirt",
        "Jeans",
        "Book",
    ]

    customers = [f"CUST_{str(i).zfill(4)}" for i in range(1, 21)]
    personas = [
        "Tech Enthusiast",
        "Fashion Conscious",
        "Fitness Enthusiast",
        "Home Cook",
        "Book Lover",
    ]
    stores = ["Store A", "Store B", "Store C", "Online"]
    payment_methods = ["Credit Card", "Debit Card", "Cash", "Mobile Payment"]
    loyalty_tiers = ["new", "regular", "vip"]

    test_data = []

    for i in range(50):  # Generate 50 random transactions with varied attributes
        transaction_id = f"TEST_TXN_{str(i+1).zfill(3)}"
        customer_id = np.random.choice(customers)

        # Random number of items (1-5)
        num_items = np.random.randint(1, 6)
        items = np.random.choice(products, size=num_items, replace=False)
        items_str = ";".join(items)

        # Random date in last 30 days
        base_date = datetime.now()
        random_days = np.random.randint(0, 30)
        date = (base_date - timedelta(days=random_days)).strftime("%Y-%m-%d")
        time = f"{np.random.randint(8, 23):02d}:{np.random.randint(0, 60):02d}"

        persona = np.random.choice(personas)
        customer_loyalty = np.random.choice(loyalty_tiers)
        store_location = np.random.choice(stores)
        payment_method = np.random.choice(payment_methods)

        test_data.append(
            {
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "items": items_str,
                "date": date,
                "time": time,
                "persona": persona,
                "customer_loyalty": customer_loyalty,
                "store_location": store_location,
                "payment_method": payment_method,
            }
        )

    return pd.DataFrame(test_data)




def generate_sample_csv():
    """Generate synthetic transaction data and save it as a CSV file for upload demo."""

    # Generate synthetic data and write to CSV for frontend upload
    df = generate_synthetic_transactions()
    test_file = "sample_data.csv"
    df.to_csv(test_file, index=False)
    print(f"✅ Created test CSV file: {test_file}")

    # Print summary statistics for quick verification
    print(f"📊 Test data summary:")
    print(f"  - Transactions: {len(df)}")
    print(f"  - Unique customers: {df['customer_id'].nunique()}")
    print(f"  - Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  - Personas: {df['persona'].unique()}")

    return test_file


if __name__ == "__main__":
    print("🧪 Generating synthetic transaction data for demo and upload\n")

    try:
        # Generate and save the sample CSV file for frontend upload demo
        print("2️⃣ Generating sample CSV file...")
        test_file = generate_sample_csv()
        print()

        print("✅ Data generation complete. Ready for demo.")
        print()
        print("🚀 Usage Instructions:")
        print("1. Start the Flask server: python app.py")
        print("2. Upload CSV via POST /upload-data or /predict-analysis")
        print("3. Check results via GET /recent-analysis")
        print("4. Monitor model status via GET /ml-status")
        print()
        print(f"📁 Test file created: {test_file}")
        print("   You can use this file to test the upload functionality")

    except Exception as e:
        print(f"❌ Data generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
