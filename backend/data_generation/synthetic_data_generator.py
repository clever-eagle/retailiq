import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os


class SyntheticDataGenerator:
    def __init__(self):
        # Product catalog with realistic relationships
        self.products = {
            "Electronics": [
                "Wireless Headphones",
                "Smartphone Case",
                "USB Cable",
                "Power Bank",
                "Bluetooth Speaker",
                "Screen Protector",
                "Wireless Charger",
                "Phone Stand",
                "Gaming Mouse",
                "Keyboard",
                "Monitor",
                "Laptop",
                "Tablet",
                "Smart Watch",
                "Camera",
                "Memory Card",
                "Hard Drive",
                "Router",
                "Smart TV",
                "Earbuds",
            ],
            "Food & Beverage": [
                "Coffee Beans",
                "Tea Bags",
                "Energy Drinks",
                "Protein Bars",
                "Snacks",
                "Chocolate",
                "Cookies",
                "Crackers",
                "Nuts",
                "Dried Fruits",
                "Candy",
                "Soft Drinks",
                "Water Bottles",
                "Juice",
                "Milk",
                "Cereal",
                "Bread",
                "Pasta",
                "Rice",
                "Instant Noodles",
            ],
            "Appliances": [
                "Coffee Maker",
                "Coffee Filters",
                "Blender",
                "Toaster",
                "Microwave",
                "Rice Cooker",
                "Air Fryer",
                "Food Processor",
                "Electric Kettle",
                "Vacuum Cleaner",
                "Hair Dryer",
                "Iron",
                "Washing Machine",
                "Dishwasher",
                "Refrigerator",
                "Air Conditioner",
                "Heater",
                "Fan",
                "Humidifier",
                "Dehumidifier",
            ],
            "Fitness": [
                "Yoga Mat",
                "Water Bottle",
                "Dumbbells",
                "Resistance Bands",
                "Protein Powder",
                "Gym Bag",
                "Workout Clothes",
                "Running Shoes",
                "Fitness Tracker",
                "Jump Rope",
                "Exercise Ball",
                "Foam Roller",
                "Weight Bench",
                "Treadmill",
                "Bike Trainer",
                "Yoga Blocks",
                "Meditation Cushion",
                "Sports Towel",
                "Energy Supplements",
                "Recovery Cream",
            ],
            "Furniture": [
                "Office Chair",
                "Desk Lamp",
                "Standing Desk",
                "Bookshelf",
                "Storage Box",
                "Filing Cabinet",
                "Couch",
                "Coffee Table",
                "Dining Table",
                "Bed Frame",
                "Mattress",
                "Wardrobe",
                "Nightstand",
                "Mirror",
                "Curtains",
                "Rug",
                "Floor Lamp",
                "Wall Clock",
                "Picture Frame",
                "Plant Pot",
            ],
            "Health & Beauty": [
                "Shampoo",
                "Conditioner",
                "Body Wash",
                "Moisturizer",
                "Sunscreen",
                "Toothbrush",
                "Toothpaste",
                "Mouthwash",
                "Face Mask",
                "Vitamin C Serum",
                "Anti-Aging Cream",
                "Hand Cream",
                "Lip Balm",
                "Perfume",
                "Deodorant",
                "Makeup",
                "Nail Polish",
                "Hair Oil",
                "Face Cleanser",
                "Body Lotion",
            ],
            "Books & Media": [
                "Business Books",
                "Fiction Novel",
                "Programming Guide",
                "Cookbook",
                "Travel Guide",
                "Biography",
                "Self-Help Book",
                "History Book",
                "Science Magazine",
                "Art Book",
                "Language Learning",
                "Comics",
                "Educational DVD",
                "Music CD",
                "Audiobook",
                "E-book Reader",
                "Notebook",
                "Planner",
                "Stickers",
                "Bookmarks",
            ],
            "Home & Garden": [
                "Indoor Plants",
                "Gardening Tools",
                "Plant Food",
                "Watering Can",
                "Garden Hose",
                "Flower Pots",
                "Seeds",
                "Soil",
                "Fertilizer",
                "Lawn Mower",
                "Garden Gloves",
                "Pruning Shears",
                "Outdoor Furniture",
                "BBQ Grill",
                "Garden Lights",
                "Bird Feeder",
                "Wind Chimes",
                "Door Mat",
                "Welcome Sign",
                "Garden Gnome",
            ],
        }

        # Product associations for market basket analysis
        self.product_associations = {
            "Coffee Maker": ["Coffee Beans", "Coffee Filters", "Sugar", "Milk"],
            "Wireless Headphones": ["Smartphone Case", "USB Cable", "Phone Stand"],
            "Yoga Mat": ["Water Bottle", "Workout Clothes", "Yoga Blocks"],
            "Office Chair": ["Desk Lamp", "Standing Desk", "Notebook"],
            "Laptop": ["Wireless Mouse", "Laptop Bag", "USB Cable", "Power Bank"],
            "Gaming Mouse": ["Keyboard", "Monitor", "Gaming Headset"],
            "Smartphone Case": ["Screen Protector", "Wireless Charger", "Earbuds"],
            "Protein Powder": ["Water Bottle", "Gym Bag", "Workout Clothes"],
            "Shampoo": ["Conditioner", "Body Wash", "Hair Oil"],
            "Toothbrush": ["Toothpaste", "Mouthwash", "Dental Floss"],
        }

        self.customer_segments = [
            "Tech Enthusiasts",
            "Fitness Focused",
            "Home & Office",
            "Health Conscious",
            "Budget Shoppers",
            "Premium Buyers",
            "Students",
            "Professionals",
            "Families",
            "Seniors",
        ]

        self.store_locations = ["Store A", "Store B", "Store C", "Store D", "Store E"]

        # Price ranges for different categories
        self.price_ranges = {
            "Electronics": (15, 500),
            "Food & Beverage": (2, 25),
            "Appliances": (25, 300),
            "Fitness": (10, 200),
            "Furniture": (50, 800),
            "Health & Beauty": (5, 80),
            "Books & Media": (8, 50),
            "Home & Garden": (5, 150),
        }

    def generate_synthetic_transactions(
        self, num_transactions=5000, start_date="2023-01-01", end_date="2024-12-31"
    ):
        """Generate synthetic transaction data"""
        transactions = []

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        # Generate customers
        num_customers = max(100, num_transactions // 20)
        customers = [f"CUST{str(i+1).zfill(4)}" for i in range(num_customers)]

        transaction_id = 1

        for _ in range(num_transactions):
            # Random date
            random_date = start + timedelta(days=random.randint(0, (end - start).days))

            # Random customer
            customer = random.choice(customers)

            # Customer segment influences product choice
            segment = random.choice(self.customer_segments)

            # Store location
            store = random.choice(self.store_locations)

            # Generate 1-5 products per transaction (market basket)
            num_items = np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.15, 0.1, 0.05])

            # Choose base product
            category = random.choice(list(self.products.keys()))
            base_product = random.choice(self.products[category])

            selected_products = [base_product]

            # Add associated products based on market basket patterns
            if base_product in self.product_associations and num_items > 1:
                associations = self.product_associations[base_product]
                additional_items = min(num_items - 1, len(associations))

                # Add some associated products
                for _ in range(additional_items):
                    if random.random() < 0.7:  # 70% chance of buying associated item
                        assoc_product = random.choice(associations)
                        if assoc_product not in selected_products:
                            selected_products.append(assoc_product)

            # Fill remaining slots with random products
            while len(selected_products) < num_items:
                random_category = random.choice(list(self.products.keys()))
                random_product = random.choice(self.products[random_category])
                if random_product not in selected_products:
                    selected_products.append(random_product)

            # Create transactions for each product
            for product in selected_products:
                # Find product category
                product_category = None
                for cat, products in self.products.items():
                    if product in products:
                        product_category = cat
                        break

                if not product_category:
                    product_category = "Electronics"  # Default

                # Generate price
                min_price, max_price = self.price_ranges[product_category]
                unit_price = round(random.uniform(min_price, max_price), 2)

                # Quantity (mostly 1, sometimes 2-3)
                quantity = np.random.choice([1, 2, 3], p=[0.8, 0.15, 0.05])

                total_amount = round(unit_price * quantity, 2)

                transaction = {
                    "transaction_id": f"TXN{str(transaction_id).zfill(6)}",
                    "date": random_date.strftime("%Y-%m-%d"),
                    "customer_id": customer,
                    "product_name": product,
                    "category": product_category,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "total_amount": total_amount,
                    "customer_segment": segment,
                    "store_location": store,
                }

                transactions.append(transaction)
                transaction_id += 1

        return pd.DataFrame(transactions)

    def save_synthetic_data(self, df, filename="synthetic_retail_data.csv"):
        """Save synthetic data to CSV file"""
        output_path = os.path.join(os.path.dirname(__file__), filename)
        df.to_csv(output_path, index=False)
        print(f"Synthetic data saved to: {output_path}")
        return output_path

    def generate_and_save(self, num_transactions=5000):
        """Generate and save synthetic data"""
        print(f"Generating {num_transactions} synthetic transactions...")
        df = self.generate_synthetic_transactions(num_transactions)

        print(f"Generated data shape: {df.shape}")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"Number of unique customers: {df['customer_id'].nunique()}")
        print(f"Number of unique products: {df['product_name'].nunique()}")
        print(f"Categories: {df['category'].unique()}")

        output_path = self.save_synthetic_data(df)

        # Also save a sample for quick testing
        sample_df = df.head(100)
        sample_path = self.save_synthetic_data(sample_df, "sample_retail_data.csv")

        return output_path, sample_path


if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    full_path, sample_path = generator.generate_and_save(
        10000
    )  # Generate 10k transactions
    print(f"Full dataset: {full_path}")
    print(f"Sample dataset: {sample_path}")
