import csv
import random
import json
from datetime import datetime, timedelta

# Define realistic product categories and items
PRODUCT_CATEGORIES = {
    "Electronics": {
        "items": [
            "iPhone 15",
            "Samsung Galaxy S24",
            "MacBook Pro",
            "Dell XPS 13",
            "iPad",
            "Microsoft Surface",
            "AirPods Pro",
            "Sony WH-1000XM5",
            "Nintendo Switch",
            "PlayStation 5",
            "Xbox Series X",
            "Apple Watch",
            "Samsung Watch",
            "Kindle",
            "iPad Mini",
            "Wireless Charger",
            "Power Bank",
            "USB-C Cable",
            "Bluetooth Speaker",
            'Smart TV 55"',
            "4K Monitor",
            "Gaming Keyboard",
            "Gaming Mouse",
            "Webcam",
            "External SSD",
            "RAM 16GB",
            "Graphics Card RTX 4070",
        ],
        "price_range": (50, 2500),
        "associations": {
            "iPhone 15": [
                "AirPods Pro",
                "Wireless Charger",
                "USB-C Cable",
                "Apple Watch",
            ],
            "MacBook Pro": [
                "External SSD",
                "USB-C Cable",
                "4K Monitor",
                "Wireless Charger",
            ],
            "Gaming Keyboard": ["Gaming Mouse", "4K Monitor", "Webcam"],
            "PlayStation 5": ["Gaming Keyboard", "Gaming Mouse", 'Smart TV 55"'],
        },
    },
    "Clothing": {
        "items": [
            "Nike Air Max",
            "Adidas Ultraboost",
            "Levi's Jeans",
            "Nike Hoodie",
            "Adidas Track Pants",
            "Under Armour T-Shirt",
            "Calvin Klein Underwear",
            "Ray-Ban Sunglasses",
            "Nike Socks",
            "Polo Ralph Lauren Shirt",
            "Converse All Stars",
            "Vans Old Skool",
            "Champion Hoodie",
            "Tommy Hilfiger Jacket",
            "Gap Jeans",
            "H&M T-Shirt",
            "Zara Dress",
            "Uniqlo Sweater",
        ],
        "price_range": (15, 300),
        "associations": {
            "Nike Air Max": ["Nike Socks", "Nike Hoodie", "Adidas Track Pants"],
            "Levi's Jeans": ["Under Armour T-Shirt", "Nike Hoodie"],
            "Ray-Ban Sunglasses": ["Polo Ralph Lauren Shirt", "Tommy Hilfiger Jacket"],
        },
    },
    "Home & Garden": {
        "items": [
            "Coffee Maker",
            "Blender",
            "Air Fryer",
            "Instant Pot",
            "Vacuum Cleaner",
            "Microwave",
            "Toaster",
            "Rice Cooker",
            "Stand Mixer",
            "Food Processor",
            "Electric Kettle",
            "Lawn Mower",
            "Garden Hose",
            "Plant Fertilizer",
            "Flower Pots",
            "Garden Tools Set",
            "Outdoor Furniture",
            "BBQ Grill",
            "Patio Umbrella",
            "Solar Lights",
        ],
        "price_range": (25, 800),
        "associations": {
            "Coffee Maker": ["Electric Kettle", "Toaster", "Microwave"],
            "Air Fryer": ["Instant Pot", "Food Processor", "Stand Mixer"],
            "Lawn Mower": ["Garden Hose", "Garden Tools Set", "Plant Fertilizer"],
        },
    },
    "Books & Media": {
        "items": [
            "The Great Gatsby",
            "To Kill a Mockingbird",
            "1984",
            "Pride and Prejudice",
            "Harry Potter Series",
            "Game of Thrones",
            "The Da Vinci Code",
            "Twilight",
            "Cookbook",
            "Self-Help Book",
            "Biography",
            "Science Fiction Novel",
            "Mystery Novel",
            "Romance Novel",
            "History Book",
            "Art Book",
            "Magazine",
        ],
        "price_range": (8, 45),
        "associations": {
            "Harry Potter Series": ["The Da Vinci Code", "Game of Thrones"],
            "Cookbook": ["Self-Help Book", "Magazine"],
        },
    },
    "Health & Beauty": {
        "items": [
            "Protein Powder",
            "Vitamins",
            "Face Cream",
            "Shampoo",
            "Conditioner",
            "Body Wash",
            "Toothpaste",
            "Deodorant",
            "Perfume",
            "Makeup Kit",
            "Skincare Set",
            "Hair Dryer",
            "Electric Toothbrush",
            "Fitness Tracker",
            "Yoga Mat",
            "Resistance Bands",
            "Dumbbells",
            "Supplement Pills",
            "Sunscreen",
            "Moisturizer",
        ],
        "price_range": (10, 200),
        "associations": {
            "Protein Powder": ["Vitamins", "Fitness Tracker", "Supplement Pills"],
            "Shampoo": ["Conditioner", "Hair Dryer", "Body Wash"],
            "Yoga Mat": ["Resistance Bands", "Fitness Tracker"],
        },
    },
    "Food & Beverages": {
        "items": [
            "Organic Coffee",
            "Green Tea",
            "Protein Bars",
            "Nuts Mix",
            "Dark Chocolate",
            "Olive Oil",
            "Pasta",
            "Tomato Sauce",
            "Bread",
            "Milk",
            "Eggs",
            "Butter",
            "Cheese",
            "Yogurt",
            "Fruits",
            "Vegetables",
            "Chicken Breast",
            "Salmon",
            "Rice",
            "Quinoa",
            "Honey",
            "Peanut Butter",
            "Cereal",
            "Orange Juice",
        ],
        "price_range": (3, 50),
        "associations": {
            "Organic Coffee": ["Milk", "Dark Chocolate", "Honey"],
            "Pasta": ["Tomato Sauce", "Olive Oil", "Cheese"],
            "Bread": ["Butter", "Peanut Butter", "Eggs"],
        },
    },
    "Sports & Outdoors": {
        "items": [
            "Tennis Racket",
            "Basketball",
            "Soccer Ball",
            "Golf Clubs",
            "Hiking Boots",
            "Camping Tent",
            "Sleeping Bag",
            "Backpack",
            "Water Bottle",
            "Bike Helmet",
            "Mountain Bike",
            "Running Shoes",
            "Ski Equipment",
            "Snowboard",
            "Surfboard",
            "Fishing Rod",
            "Swimming Goggles",
            "Tennis Balls",
            "Golf Balls",
            "Gym Bag",
        ],
        "price_range": (20, 1200),
        "associations": {
            "Tennis Racket": ["Tennis Balls", "Gym Bag", "Water Bottle"],
            "Hiking Boots": ["Backpack", "Water Bottle", "Camping Tent"],
            "Mountain Bike": ["Bike Helmet", "Water Bottle", "Backpack"],
        },
    },
}

# Customer personas with different shopping behaviors
CUSTOMER_PERSONAS = [
    {
        "name": "Tech Enthusiast",
        "preferred_categories": ["Electronics"],
        "avg_items_per_transaction": 3.5,
        "frequency": 0.15,
        "budget_multiplier": 2.0,
    },
    {
        "name": "Fashion Conscious",
        "preferred_categories": ["Clothing", "Health & Beauty"],
        "avg_items_per_transaction": 4.2,
        "frequency": 0.20,
        "budget_multiplier": 1.3,
    },
    {
        "name": "Home Cook",
        "preferred_categories": ["Home & Garden", "Food & Beverages"],
        "avg_items_per_transaction": 6.8,
        "frequency": 0.25,
        "budget_multiplier": 1.0,
    },
    {
        "name": "Fitness Enthusiast",
        "preferred_categories": ["Health & Beauty", "Sports & Outdoors"],
        "avg_items_per_transaction": 3.1,
        "frequency": 0.18,
        "budget_multiplier": 1.5,
    },
    {
        "name": "Book Lover",
        "preferred_categories": ["Books & Media", "Food & Beverages"],
        "avg_items_per_transaction": 2.8,
        "frequency": 0.12,
        "budget_multiplier": 0.8,
    },
    {
        "name": "General Shopper",
        "preferred_categories": list(PRODUCT_CATEGORIES.keys()),
        "avg_items_per_transaction": 4.5,
        "frequency": 0.10,
        "budget_multiplier": 1.2,
    },
]


def generate_realistic_transaction(customer_persona, transaction_id):
    """Generate a realistic transaction based on customer persona with dynamic variations"""

    # Select categories based on persona preferences
    if customer_persona["name"] == "General Shopper":
        selected_categories = random.choices(
            customer_persona["preferred_categories"], k=random.randint(1, 3)
        )
    else:
        selected_categories = customer_persona["preferred_categories"]

    # Determine number of items with more variation
    base_items = customer_persona["avg_items_per_transaction"]
    variation = random.uniform(0.5, 1.5)  # Add 50% variation
    num_items = max(
        1, int(random.normalvariate(base_items * variation, base_items * 0.4))
    )

    transaction_items = []
    selected_items = set()

    # Seasonal/time-based preferences
    current_season = random.choice(["spring", "summer", "fall", "winter"])
    seasonal_boost = {
        "spring": ["Garden Tools Set", "Plant Fertilizer", "Outdoor Furniture"],
        "summer": ["BBQ Grill", "Swimming Goggles", "Sunscreen", "Surfboard"],
        "fall": ["Hiking Boots", "Jacket", "Coffee Maker"],
        "winter": ["Ski Equipment", "Heating", "Hot Chocolate"],
    }

    # Weekend vs weekday shopping patterns
    is_weekend = random.choice([True, False])
    weekend_preference = (
        0.3 if is_weekend else 0.1
    )  # More likely to buy leisure items on weekends

    for _ in range(num_items):
        # Select category with seasonal influence
        category = random.choice(selected_categories)
        category_data = PRODUCT_CATEGORIES[category]

        # Select item from category
        available_items = [
            item for item in category_data["items"] if item not in selected_items
        ]
        if not available_items:
            continue

        # Apply seasonal preferences
        item = random.choice(available_items)

        # Boost certain items based on season
        if any(
            seasonal_item in item
            for seasonal_item in seasonal_boost.get(current_season, [])
        ):
            if random.random() < 0.7:  # 70% chance to prefer seasonal items
                seasonal_items = [
                    i
                    for i in available_items
                    if any(s in i for s in seasonal_boost[current_season])
                ]
                if seasonal_items:
                    item = random.choice(seasonal_items)

        selected_items.add(item)

        # Dynamic association probability based on customer type and time
        association_probability = (
            0.6 if customer_persona["name"] == "Tech Enthusiast" else 0.4
        )
        if is_weekend:
            association_probability += (
                0.2  # More likely to buy related items on weekends
            )

        # Check for associated items (market basket associations)
        if item in category_data.get("associations", {}):
            associated_items = category_data["associations"][item]
            if (
                random.random() < association_probability
                and len(selected_items) < num_items
            ):
                # Select multiple associated items sometimes
                num_associated = random.choices([1, 2, 3], weights=[0.7, 0.25, 0.05])[0]
                for _ in range(num_associated):
                    if associated_items and len(selected_items) < num_items:
                        associated_item = random.choice(associated_items)
                        if associated_item not in selected_items:
                            transaction_items.append(associated_item)
                            selected_items.add(associated_item)

        transaction_items.append(item)

    # Add random impulse purchases (10% chance)
    if random.random() < 0.1:
        impulse_categories = ["Food & Beverages", "Health & Beauty"]
        impulse_category = random.choice(impulse_categories)
        impulse_items = PRODUCT_CATEGORIES[impulse_category]["items"]
        impulse_item = random.choice(impulse_items)
        if impulse_item not in selected_items:
            transaction_items.append(impulse_item)

    # Remove duplicates while preserving order
    seen = set()
    unique_items = []
    for item in transaction_items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    return unique_items


def generate_large_dataset(num_transactions=1000):
    """Generate a dynamic, manageable dataset with realistic variations"""

    print(f"Generating {num_transactions} dynamic realistic transactions...")

    transactions = []

    # Generate diverse customer base with varying behaviors
    customers = []
    for i in range(num_transactions // 4):  # Average 4 transactions per customer
        persona = random.choices(
            CUSTOMER_PERSONAS, weights=[p["frequency"] for p in CUSTOMER_PERSONAS]
        )[0]

        # Add customer loyalty level (affects purchase patterns)
        loyalty_level = random.choices(
            ["new", "regular", "vip"], weights=[0.3, 0.5, 0.2]
        )[0]

        customers.append(
            {
                "id": f"CUST_{i:04d}",
                "persona": persona,
                "loyalty": loyalty_level,
                "avg_spending": random.uniform(50, 500),
            }
        )

    # Generate transactions with temporal patterns
    for transaction_id in range(1, num_transactions + 1):
        if transaction_id % 100 == 0:
            print(f"Generated {transaction_id} transactions...")

        # Select customer with returning customer preference
        if (
            random.random() < 0.4 and len(customers) > 0
        ):  # 40% chance returning customer
            customer = random.choice(
                customers[: len(customers) // 2]
            )  # Favor earlier customers
        else:
            customer = random.choice(customers)

        # Generate transaction with customer-specific modifications
        items = generate_realistic_transaction(customer["persona"], transaction_id)

        # VIP customers tend to buy more items
        if customer["loyalty"] == "vip" and random.random() < 0.3:
            extra_items = generate_realistic_transaction(
                customer["persona"], transaction_id
            )
            items.extend(extra_items[:2])  # Add up to 2 extra items
            items = list(set(items))  # Remove duplicates

        if len(items) > 0:  # Only add non-empty transactions
            # Create dynamic transaction dates with realistic patterns
            base_date = datetime.now() - timedelta(days=180)

            # Weekend clustering (more transactions on weekends)
            if random.random() < 0.3:  # 30% weekend transactions
                days_to_weekend = random.randint(0, 180)
                days_to_weekend = (days_to_weekend // 7) * 7 + random.choice(
                    [5, 6]
                )  # Saturday or Sunday
                transaction_date = base_date + timedelta(days=min(days_to_weekend, 180))
            else:
                random_days = random.randint(0, 180)
                transaction_date = base_date + timedelta(days=random_days)

            # Add transaction times for more realism
            hour = random.choices(
                range(24),
                weights=[
                    2,
                    1,
                    1,
                    1,
                    2,
                    3,
                    4,
                    6,
                    8,
                    10,
                    12,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    17,
                    15,
                    12,
                    8,
                    6,
                    4,
                    3,
                ],
            )[
                0
            ]  # Peak hours weighted

            transactions.append(
                {
                    "transaction_id": f"TXN_{transaction_id:06d}",
                    "customer_id": customer["id"],
                    "items": items,
                    "date": transaction_date.strftime("%Y-%m-%d"),
                    "time": f"{hour:02d}:{random.randint(0,59):02d}",
                    "persona": customer["persona"]["name"],
                    "customer_loyalty": customer["loyalty"],
                    "store_location": random.choice(
                        ["Store A", "Store B", "Store C", "Online"]
                    ),
                    "payment_method": random.choices(
                        ["Credit Card", "Debit Card", "Cash", "Mobile Payment"],
                        weights=[0.4, 0.3, 0.15, 0.15],
                    )[0],
                }
            )

    return transactions


def save_transactions_to_csv(transactions, filename):
    """Save transactions to CSV format for market basket analysis with enhanced fields"""

    print(f"Saving {len(transactions)} enhanced transactions to {filename}...")

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write enhanced header
        writer.writerow(
            [
                "transaction_id",
                "customer_id",
                "items",
                "date",
                "time",
                "persona",
                "customer_loyalty",
                "store_location",
                "payment_method",
            ]
        )

        # Write transactions
        for transaction in transactions:
            # Join items with semicolon for CSV format
            items_str = ";".join(transaction["items"])
            writer.writerow(
                [
                    transaction["transaction_id"],
                    transaction["customer_id"],
                    items_str,
                    transaction["date"],
                    transaction.get("time", "12:00"),
                    transaction["persona"],
                    transaction.get("customer_loyalty", "regular"),
                    transaction.get("store_location", "Store A"),
                    transaction.get("payment_method", "Credit Card"),
                ]
            )


def generate_statistics(transactions):
    """Generate dataset statistics"""

    total_transactions = len(transactions)
    all_items = []
    persona_counts = {}

    for transaction in transactions:
        all_items.extend(transaction["items"])
        persona = transaction["persona"]
        persona_counts[persona] = persona_counts.get(persona, 0) + 1

    unique_items = len(set(all_items))
    avg_items_per_transaction = len(all_items) / total_transactions

    # Top items
    from collections import Counter

    item_counts = Counter(all_items)
    top_items = item_counts.most_common(20)

    statistics = {
        "total_transactions": total_transactions,
        "unique_items": unique_items,
        "total_items_sold": len(all_items),
        "avg_items_per_transaction": round(avg_items_per_transaction, 2),
        "persona_distribution": persona_counts,
        "top_items": top_items,
        "dataset_generation_date": datetime.now().isoformat(),
    }

    return statistics


if __name__ == "__main__":
    # Generate small, manageable dataset
    print("Starting small dataset generation...")

    # Generate 1,000 transactions for better performance
    transactions = generate_large_dataset(1200)

    # Save to CSV
    csv_filename = "sample3.csv"
    save_transactions_to_csv(transactions, csv_filename)

    # Generate and save statistics
    stats = generate_statistics(transactions)

    with open("dataset_statistics.json", "w") as f:
        json.dump(stats, f, indent=2)

    print("\n" + "=" * 60)
    print("DATASET GENERATION COMPLETE!")
    print("=" * 60)
    print(f"Total Transactions: {stats['total_transactions']:,}")
    print(f"Unique Items: {stats['unique_items']:,}")
    print(f"Total Items Sold: {stats['total_items_sold']:,}")
    print(f"Avg Items per Transaction: {stats['avg_items_per_transaction']}")
    print("\nCustomer Persona Distribution:")
    for persona, count in stats["persona_distribution"].items():
        percentage = (count / stats["total_transactions"]) * 100
        print(f"  {persona}: {count:,} transactions ({percentage:.1f}%)")

    print(f"\nTop 10 Most Popular Items:")
    for item, count in stats["top_items"][:10]:
        percentage = (count / stats["total_items_sold"]) * 100
        print(f"  {item}: {count:,} times ({percentage:.1f}%)")

    print(f"\nFiles generated:")
    print(f"  - {csv_filename}")
    print(f"  - dataset_statistics.json")
    print("\nDataset is ready for market basket analysis!")
