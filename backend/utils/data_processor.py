import pandas as pd
import numpy as np
from datetime import datetime
import os
import json


class DataProcessor:
    """
    Data processing utilities for the retail analytics backend
    """

    def __init__(self):
        self.required_columns = [
            "transaction_id",
            "date",
            "customer_id",
            "product_name",
            "category",
            "quantity",
            "unit_price",
        ]

    def validate_and_clean_data(self, df):
        """
                   for keyword in keywords:
                if keyword in item_lower:
                    return category

        return 'Other' uploaded data
        """
        try:
            # Check if all required columns exist
            missing_columns = [
                col for col in self.required_columns if col not in df.columns
            ]
            if missing_columns:
                # Try to infer column mappings
                df = self._infer_column_mappings(df)

                # Check again after inference
                missing_columns = [
                    col for col in self.required_columns if col not in df.columns
                ]
                if missing_columns:
                    raise ValueError(f"Missing required columns: {missing_columns}")

            # Clean data
            df = df.copy()

            # Remove rows with missing critical values
            df = df.dropna(
                subset=["transaction_id", "product_name", "quantity", "unit_price"]
            )

            # Convert data types
            df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
            df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

            # Remove rows with invalid numeric values
            df = df.dropna(subset=["quantity", "unit_price"])
            df = df[df["quantity"] > 0]
            df = df[df["unit_price"] > 0]

            # Create total_amount if not exists
            if "total_amount" not in df.columns:
                df["total_amount"] = df["quantity"] * df["unit_price"]

            # Convert date column
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df = df.dropna(subset=["date"])

            # Clean text columns
            text_columns = ["product_name", "category", "customer_id", "transaction_id"]
            for col in text_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()

            return df

        except Exception as e:
            raise ValueError(f"Data validation failed: {str(e)}")

    def _infer_column_mappings(self, df):
        """
        Try to infer column mappings from common variations
        """
        column_mappings = {
            "transaction_id": [
                "txn_id",
                "trans_id",
                "order_id",
                "invoice_id",
                "receipt_id",
            ],
            "customer_id": ["cust_id", "customer", "user_id", "client_id"],
            "product_name": ["product", "item", "item_name", "product_description"],
            "category": ["cat", "product_category", "item_category", "type"],
            "quantity": ["qty", "amount", "count"],
            "unit_price": ["price", "item_price", "cost", "rate"],
            "total_amount": ["total", "total_price", "amount", "revenue"],
            "date": ["order_date", "purchase_date", "timestamp", "created_date"],
        }

        df_columns_lower = [col.lower() for col in df.columns]

        for standard_col, variations in column_mappings.items():
            if standard_col not in df.columns:
                for variation in variations:
                    if variation.lower() in df_columns_lower:
                        original_col = df.columns[
                            df_columns_lower.index(variation.lower())
                        ]
                        df = df.rename(columns={original_col: standard_col})
                        break

        return df

    def load_default_data(self):
        """
        Load default retail transaction data - prioritize dynamic large dataset
        """
        try:
            # First try to load the dynamic large market basket dataset
            large_data_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "large_market_basket_data.csv",
            )

            if os.path.exists(large_data_path):
                print(
                    f"Loading dynamic large market basket dataset from: {large_data_path}"
                )
                df = pd.read_csv(large_data_path)

                # Process the large dataset format
                processed_data = self.process_large_market_basket_data(df)
                return processed_data

            # Fallback to demo electronics data (small, fast)
            demo_electronics_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "demo_data_electronics.csv",
            )

            if os.path.exists(demo_electronics_path):
                print(f"Loading demo electronics dataset from: {demo_electronics_path}")
                df = pd.read_csv(demo_electronics_path)
                return self.validate_and_clean_data(df)

            # Fallback to sample market basket data
            sample_data_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "sample_market_basket_data.csv",
            )

            if os.path.exists(sample_data_path):
                print(f"Loading sample market basket data from: {sample_data_path}")
                df = pd.read_csv(sample_data_path)
                return self.validate_and_clean_data(df)

            # Try to load from frontend data folder
            frontend_data_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "frontend",
                "public",
                "data",
                "retail_transactions.csv",
            )

            if os.path.exists(frontend_data_path):
                df = pd.read_csv(frontend_data_path)
                return self.validate_and_clean_data(df)

            # Try alternative path
            alt_data_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "frontend",
                "data",
                "fabricated_sales_data.csv",
            )

            if os.path.exists(alt_data_path):
                df = pd.read_csv(alt_data_path)
                return self.validate_and_clean_data(df)

            # If no files found, create sample data
            return self._create_sample_data()

        except Exception as e:
            print(f"Error loading default data: {e}")
            return self._create_sample_data()

    def _create_sample_data(self):
        """
        Create sample retail transaction data
        """
        try:
            np.random.seed(42)

            # Sample products and categories
            products = {
                "Electronics": [
                    "Laptop",
                    "Smartphone",
                    "Headphones",
                    "Tablet",
                    "Smart Watch",
                ],
                "Clothing": ["T-Shirt", "Jeans", "Sneakers", "Jacket", "Dress"],
                "Food": ["Coffee", "Bread", "Milk", "Apples", "Pasta"],
                "Books": ["Novel", "Cookbook", "Biography", "Science Book", "Magazine"],
                "Home": ["Lamp", "Pillow", "Curtains", "Plate Set", "Candle"],
            }

            data = []

            # Generate 1000 sample transactions
            for i in range(1000):
                transaction_id = f"TXN{i+1:04d}"
                customer_id = f"CUST{np.random.randint(1, 201):03d}"

                # Random date in the last 6 months
                base_date = datetime.now()
                random_days = np.random.randint(0, 180)
                transaction_date = base_date - pd.Timedelta(days=random_days)

                # Random category and product
                category = np.random.choice(list(products.keys()))
                product_name = np.random.choice(products[category])

                # Random quantity and price
                quantity = np.random.randint(1, 5)

                # Price ranges by category
                price_ranges = {
                    "Electronics": (50, 1000),
                    "Clothing": (15, 200),
                    "Food": (2, 30),
                    "Books": (10, 50),
                    "Home": (10, 150),
                }

                min_price, max_price = price_ranges[category]
                unit_price = round(np.random.uniform(min_price, max_price), 2)
                total_amount = round(quantity * unit_price, 2)

                data.append(
                    {
                        "transaction_id": transaction_id,
                        "date": transaction_date.strftime("%Y-%m-%d"),
                        "customer_id": customer_id,
                        "product_name": product_name,
                        "category": category,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total_amount": total_amount,
                    }
                )

            df = pd.DataFrame(data)
            return self.validate_and_clean_data(df)

        except Exception as e:
            print(f"Error creating sample data: {e}")
            return pd.DataFrame()

    def get_data_summary(self, df):
        """
        Get summary statistics of the data
        """
        try:
            summary = {
                "basic_info": {
                    "total_rows": len(df),
                    "total_columns": len(df.columns),
                    "date_range": {
                        "start": (
                            df["date"].min().isoformat()
                            if "date" in df.columns
                            else None
                        ),
                        "end": (
                            df["date"].max().isoformat()
                            if "date" in df.columns
                            else None
                        ),
                    },
                },
                "transactions": {
                    "total_transactions": (
                        df["transaction_id"].nunique()
                        if "transaction_id" in df.columns
                        else 0
                    ),
                    "total_customers": (
                        df["customer_id"].nunique()
                        if "customer_id" in df.columns
                        else 0
                    ),
                    "avg_transaction_value": (
                        float(df["total_amount"].mean())
                        if "total_amount" in df.columns
                        else 0
                    ),
                },
                "products": {
                    "total_products": (
                        df["product_name"].nunique()
                        if "product_name" in df.columns
                        else 0
                    ),
                    "total_categories": (
                        df["category"].nunique() if "category" in df.columns else 0
                    ),
                    "top_products": (
                        df["product_name"].value_counts().head(10).to_dict()
                        if "product_name" in df.columns
                        else {}
                    ),
                    "top_categories": (
                        df["category"].value_counts().to_dict()
                        if "category" in df.columns
                        else {}
                    ),
                },
                "revenue": {
                    "total_revenue": (
                        float(df["total_amount"].sum())
                        if "total_amount" in df.columns
                        else 0
                    ),
                    "avg_order_value": (
                        float(df.groupby("transaction_id")["total_amount"].sum().mean())
                        if all(
                            col in df.columns
                            for col in ["transaction_id", "total_amount"]
                        )
                        else 0
                    ),
                    "revenue_by_category": (
                        df.groupby("category")["total_amount"].sum().to_dict()
                        if all(
                            col in df.columns for col in ["category", "total_amount"]
                        )
                        else {}
                    ),
                },
            }

            return summary

        except Exception as e:
            print(f"Error generating data summary: {e}")
            return {"error": str(e)}

    def export_data(self, df, format="csv"):
        """
        Export processed data
        """
        try:
            if format == "csv":
                return df.to_csv(index=False)
            elif format == "json":
                return df.to_json(orient="records", date_format="iso")
            else:
                raise ValueError(f"Unsupported format: {format}")

        except Exception as e:
            raise ValueError(f"Export failed: {str(e)}")

    def preprocess_for_ml(self, df):
        """
        Preprocess data specifically for machine learning models
        """
        try:
            processed_df = df.copy()

            # Create additional features for ML
            processed_df["hour"] = pd.to_datetime(processed_df["date"]).dt.hour
            processed_df["day_of_week"] = pd.to_datetime(
                processed_df["date"]
            ).dt.dayofweek
            processed_df["month"] = pd.to_datetime(processed_df["date"]).dt.month
            processed_df["quarter"] = pd.to_datetime(processed_df["date"]).dt.quarter

            # Customer transaction frequency
            customer_freq = (
                processed_df.groupby("customer_id").size().rename("customer_frequency")
            )
            processed_df = processed_df.merge(
                customer_freq, on="customer_id", how="left"
            )

            # Product popularity
            product_freq = (
                processed_df.groupby("product_name").size().rename("product_popularity")
            )
            processed_df = processed_df.merge(
                product_freq, on="product_name", how="left"
            )

            # Category average price
            category_avg_price = (
                processed_df.groupby("category")["unit_price"]
                .mean()
                .rename("category_avg_price")
            )
            processed_df = processed_df.merge(
                category_avg_price, on="category", how="left"
            )

            return processed_df

        except Exception as e:
            raise ValueError(f"ML preprocessing failed: {str(e)}")

    def process_large_market_basket_data(self, df):
        """
        Process the large market basket dataset format for analysis
        """
        try:
            print("Processing large market basket dataset...")

            # The large dataset has format: transaction_id, customer_id, items, date, persona
            # Convert to standard format for market basket analysis
            processed_rows = []

            for _, row in df.iterrows():
                transaction_id = row["transaction_id"]
                customer_id = row["customer_id"]
                date = row["date"]
                persona = row["persona"]

                # Split items by semicolon
                items = row["items"].split(";")

                # Create a row for each item in the transaction
                for item in items:
                    processed_rows.append(
                        {
                            "transaction_id": transaction_id,
                            "customer_id": customer_id,
                            "product_name": item.strip(),
                            "date": date,
                            "persona": persona,
                            "quantity": 1,  # Default quantity
                            "unit_price": self._estimate_price_from_item(item.strip()),
                            "category": self._categorize_item(item.strip()),
                        }
                    )

            processed_df = pd.DataFrame(processed_rows)

            # Convert date column to datetime
            if "date" in processed_df.columns:
                processed_df["date"] = pd.to_datetime(
                    processed_df["date"], errors="coerce"
                )
                processed_df = processed_df.dropna(subset=["date"])

            # Calculate total_amount if not present
            if (
                "total_amount" not in processed_df.columns
                and "unit_price" in processed_df.columns
                and "quantity" in processed_df.columns
            ):
                processed_df["total_amount"] = (
                    processed_df["unit_price"] * processed_df["quantity"]
                )

            print(
                f"Processed {len(processed_df)} item records from {len(df)} transactions"
            )
            print(f"Found {processed_df['product_name'].nunique()} unique products")
            print(f"Customer personas: {processed_df['persona'].unique()}")

            return processed_df

        except Exception as e:
            print(f"Error processing large market basket data: {str(e)}")
            raise ValueError(f"Failed to process large dataset: {str(e)}")

    def _estimate_price_from_item(self, item_name):
        """
        Estimate price based on item name and category
        """
        # Price estimation based on product categories
        price_ranges = {
            # Electronics
            "iphone": (800, 1200),
            "samsung galaxy": (700, 1100),
            "macbook": (1200, 2500),
            "ipad": (300, 800),
            "airpods": (150, 250),
            "watch": (250, 500),
            "nintendo": (300, 400),
            "playstation": (400, 500),
            "xbox": (400, 500),
            "tv": (400, 1200),
            "monitor": (200, 600),
            "keyboard": (50, 200),
            # Clothing
            "nike": (60, 200),
            "adidas": (50, 180),
            "jeans": (40, 120),
            "hoodie": (30, 80),
            "shirt": (20, 60),
            "jacket": (50, 200),
            "shoes": (50, 300),
            "sunglasses": (50, 250),
            # Home & Garden
            "coffee maker": (50, 300),
            "blender": (30, 150),
            "vacuum": (100, 400),
            "microwave": (80, 250),
            "toaster": (25, 80),
            "lawn mower": (200, 800),
            "grill": (150, 600),
            # Health & Beauty
            "protein": (25, 80),
            "vitamins": (15, 50),
            "shampoo": (8, 25),
            "perfume": (50, 200),
            "makeup": (20, 100),
            # Food & Beverages
            "coffee": (10, 30),
            "chocolate": (3, 15),
            "oil": (5, 20),
            "pasta": (2, 8),
            "milk": (3, 6),
            "bread": (2, 5),
            # Sports & Outdoors
            "tennis": (30, 200),
            "basketball": (20, 50),
            "bike": (200, 1200),
            "tent": (100, 500),
            "backpack": (50, 200),
        }

        item_lower = item_name.lower()

        # Find matching price range
        for keyword, (min_price, max_price) in price_ranges.items():
            if keyword in item_lower:
                return round(np.random.uniform(min_price, max_price), 2)

        # Default price range for unknown items
        return round(np.random.uniform(10, 100), 2)

    def _categorize_item(self, item_name):
        """
        Categorize item based on its name
        """
        item_lower = item_name.lower()

        categories = {
            "Electronics": [
                "iphone",
                "samsung",
                "macbook",
                "ipad",
                "airpods",
                "watch",
                "nintendo",
                "playstation",
                "xbox",
                "tv",
                "monitor",
                "keyboard",
                "mouse",
                "charger",
                "cable",
                "speaker",
                "headphones",
                "kindle",
                "graphics",
            ],
            "Clothing": [
                "nike",
                "adidas",
                "jeans",
                "hoodie",
                "shirt",
                "jacket",
                "shoes",
                "sunglasses",
                "socks",
                "polo",
                "converse",
                "vans",
                "champion",
                "tommy",
                "gap",
                "dress",
                "sweater",
                "underwear",
            ],
            "Home & Garden": [
                "coffee maker",
                "blender",
                "fryer",
                "pot",
                "vacuum",
                "microwave",
                "toaster",
                "rice cooker",
                "mixer",
                "kettle",
                "lawn mower",
                "hose",
                "fertilizer",
                "tools",
                "furniture",
                "grill",
                "umbrella",
                "lights",
            ],
            "Books & Media": [
                "gatsby",
                "mockingbird",
                "1984",
                "pride",
                "harry potter",
                "twilight",
                "cookbook",
                "biography",
                "novel",
                "book",
                "magazine",
            ],
            "Health & Beauty": [
                "protein",
                "vitamins",
                "cream",
                "shampoo",
                "conditioner",
                "wash",
                "toothpaste",
                "deodorant",
                "perfume",
                "makeup",
                "skincare",
                "dryer",
                "toothbrush",
                "tracker",
                "yoga",
                "resistance",
                "dumbbells",
                "sunscreen",
            ],
            "Food & Beverages": [
                "coffee",
                "tea",
                "protein bars",
                "nuts",
                "chocolate",
                "oil",
                "pasta",
                "sauce",
                "bread",
                "milk",
                "eggs",
                "butter",
                "cheese",
                "yogurt",
                "fruits",
                "vegetables",
                "chicken",
                "salmon",
                "rice",
                "quinoa",
                "honey",
                "peanut",
                "cereal",
                "juice",
            ],
            "Sports & Outdoors": [
                "tennis",
                "basketball",
                "soccer",
                "golf",
                "hiking",
                "camping",
                "tent",
                "sleeping bag",
                "backpack",
                "bottle",
                "helmet",
                "bike",
                "running",
                "ski",
                "snowboard",
                "surfboard",
                "fishing",
                "swimming",
                "balls",
                "gym bag",
            ],
        }

        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in item_lower:
                    return category

        return "Other"
