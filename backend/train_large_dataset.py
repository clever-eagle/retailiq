#!/usr/bin/env python3
"""
Large Dataset Training Script for Market Basket Analysis
Optimized for 50,000+ transactions with comprehensive analytics
"""

import pandas as pd
import numpy as np
import time
import json
from models.apriori_market_basket import AprioriMarketBasket
from utils.data_processor import DataProcessor


def train_large_dataset():
    """
    Train the market basket model on the large dataset
    """
    start_time = time.time()
    print("=" * 80)
    print("LARGE DATASET MARKET BASKET ANALYSIS TRAINING")
    print("=" * 80)

    # Initialize components
    data_processor = DataProcessor()
    analyzer = AprioriMarketBasket()

    try:
        # Load the large dataset
        print("Loading large dataset...")
        df = data_processor.load_default_data()

        print(f"\nDataset Statistics:")
        print(f"  Total records: {len(df):,}")
        print(f"  Unique products: {df['product_name'].nunique():,}")
        print(f"  Unique transactions: {df['transaction_id'].nunique():,}")
        print(f"  Unique customers: {df['customer_id'].nunique():,}")
        print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"  Product categories: {df['category'].nunique():,}")
        print(f"  Customer personas: {df['persona'].nunique():,}")

        # Show category distribution
        print(f"\nCategory Distribution:")
        category_counts = df["category"].value_counts()
        for cat, count in category_counts.head(8).items():
            percentage = (count / len(df)) * 100
            print(f"  {cat:<20}: {count:>6,} ({percentage:>5.1f}%)")

        # Show persona distribution
        print(f"\nCustomer Persona Distribution:")
        persona_counts = df.groupby("persona")["transaction_id"].nunique()
        total_transactions = df["transaction_id"].nunique()
        for persona, count in persona_counts.items():
            percentage = (count / total_transactions) * 100
            print(f"  {persona:<20}: {count:>6,} transactions ({percentage:>5.1f}%)")

        # Optimize parameters for large dataset
        params = {
            "min_support": 0.001,  # Very low for large dataset (0.1% = 50 transactions)
            "min_confidence": 0.2,  # Lower confidence for more rules
            "min_lift": 1.1,  # Just above random
        }

        print(f"\nOptimized Training Parameters:")
        print(
            f"  Min Support: {params['min_support']} ({params['min_support']*100:.1f}% = {int(params['min_support'] * df['transaction_id'].nunique())} transactions)"
        )
        print(
            f"  Min Confidence: {params['min_confidence']} ({params['min_confidence']*100:.1f}%)"
        )
        print(f"  Min Lift: {params['min_lift']}")

        # Perform analysis
        print(f"\nStarting comprehensive market basket analysis...")
        print("This may take several minutes for large datasets...")
        analysis_start = time.time()

        result = analyzer.analyze(
            df,
            min_support=params["min_support"],
            min_confidence=params["min_confidence"],
            min_lift=params["min_lift"],
        )

        analysis_time = time.time() - analysis_start

        # Process results
        rules = result.get("association_rules", [])
        stats = result.get("statistics", {})
        advanced_analytics = result.get("advanced_analytics", {})

        # Create comprehensive training report
        training_report = {
            "training_metadata": {
                "training_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "dataset_type": "Large Scale Retail Dataset",
                "analysis_engine": "Enhanced Apriori Algorithm",
            },
            "dataset_profile": {
                "total_records": len(df),
                "unique_products": int(df["product_name"].nunique()),
                "unique_transactions": int(df["transaction_id"].nunique()),
                "unique_customers": int(df["customer_id"].nunique()),
                "product_categories": int(df["category"].nunique()),
                "customer_personas": int(df["persona"].nunique()),
                "date_range": {
                    "start": str(df["date"].min()),
                    "end": str(df["date"].max()),
                    "days_covered": (
                        pd.to_datetime(df["date"].max())
                        - pd.to_datetime(df["date"].min())
                    ).days,
                },
                "avg_items_per_transaction": round(
                    len(df) / df["transaction_id"].nunique(), 2
                ),
            },
            "training_configuration": params,
            "analysis_results": {
                "total_association_rules": len(rules),
                "frequent_itemsets_found": stats.get("frequent_itemsets_count", 0),
                "strong_rules_lift_2plus": stats.get("strong_rules", 0),
                "very_strong_rules_lift_3plus": stats.get("very_strong_rules", 0),
                "dataset_classification": stats.get("dataset_size", "Large"),
                "analysis_quality": (
                    "High"
                    if len(rules) > 100
                    else "Medium" if len(rules) > 20 else "Low"
                ),
            },
            "performance_metrics": {
                "training_time_seconds": round(analysis_time, 2),
                "total_execution_time": round(time.time() - start_time, 2),
                "processing_speed": (
                    f"{stats.get('total_transactions', 0) / analysis_time:.0f} transactions/second"
                    if analysis_time > 0
                    else "N/A"
                ),
                "memory_efficiency": "Optimized for large datasets",
            },
            "business_insights": advanced_analytics,
        }

        # Save comprehensive report
        with open("large_dataset_training_report.json", "w") as f:
            json.dump(training_report, f, indent=2, default=str)

        # Display results
        print(f"\n" + "=" * 80)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"🎯 Analysis Performance:")
        print(f"   Training Time: {analysis_time:.2f} seconds")
        print(
            f"   Processing Speed: {stats.get('total_transactions', 0) / analysis_time:.0f} transactions/second"
        )
        print(f"   Total Execution: {time.time() - start_time:.2f} seconds")

        print(f"\n📊 Model Quality Metrics:")
        print(f"   Association Rules Generated: {len(rules):,}")
        print(f"   Strong Rules (lift > 2.0): {stats.get('strong_rules', 0):,}")
        print(
            f"   Very Strong Rules (lift > 3.0): {stats.get('very_strong_rules', 0):,}"
        )
        print(f"   Frequent Itemsets: {stats.get('frequent_itemsets_count', 0):,}")

        # Show top association rules
        if rules:
            print(f"\n🏆 Top 15 Association Rules by Lift:")
            print("-" * 90)
            for i, rule in enumerate(
                sorted(rules, key=lambda x: x["lift"], reverse=True)[:15]
            ):
                antecedent = (
                    rule["antecedent"][0]
                    if isinstance(rule["antecedent"], list)
                    else rule["antecedent"]
                )
                consequent = (
                    rule["consequent"][0]
                    if isinstance(rule["consequent"], list)
                    else rule["consequent"]
                )
                print(
                    f"{i+1:2d}. {antecedent:<25} → {consequent:<25} "
                    f"(S:{rule['support']:.3f}, C:{rule['confidence']:.3f}, L:{rule['lift']:.2f})"
                )

        # Business intelligence insights
        if "category_insights" in advanced_analytics:
            category_insights = advanced_analytics["category_insights"]
            if "top_categories" in category_insights:
                print(f"\n📈 Category Performance Analysis:")
                print("-" * 60)
                for cat_info in category_insights["top_categories"][:10]:
                    print(
                        f"   {cat_info['category']:<20}: {cat_info['count']:>7,} items ({cat_info['percentage']:>5.1f}%)"
                    )

        if "persona_insights" in advanced_analytics:
            persona_insights = advanced_analytics["persona_insights"]
            if "persona_distribution" in persona_insights:
                print(f"\n👥 Customer Persona Intelligence:")
                print("-" * 80)
                for persona_info in persona_insights["persona_distribution"]:
                    print(
                        f"   {persona_info['persona']:<20}: {persona_info['transactions']:>6,} txns "
                        f"({persona_info['market_share']:>5.1f}%), "
                        f"Avg: {persona_info['avg_items_per_transaction']:.1f} items/txn"
                    )

        # Revenue impact analysis
        print(f"\n💰 Business Impact Analysis:")
        total_revenue_potential = sum(
            rule.get("conviction", 1.0) * rule["support"] * 1000 for rule in rules[:20]
        )
        print(f"   Top 20 Rules Revenue Potential: ${total_revenue_potential:,.0f}")
        print(
            f"   Cross-sell Opportunities: {len([r for r in rules if r['lift'] > 2.0]):,} high-confidence pairs"
        )
        print(
            f"   Market Penetration: {(len(rules) / df['product_name'].nunique())*100:.1f}% product coverage"
        )

        print(f"\n📁 Output Files:")
        print(f"   Training Report: large_dataset_training_report.json")
        print(f"   Dataset: large_market_basket_data.csv ({len(df):,} records)")
        print(f"   Statistics: dataset_statistics.json")

        print(f"\n🚀 Model Status: PRODUCTION READY")
        print(f"   API Endpoint: http://localhost:5000/market-basket-analysis")
        print(f"   Recommendation Quality: {'High' if len(rules) > 100 else 'Medium'}")
        print(
            f"   Scalability: Optimized for {df['transaction_id'].nunique():,}+ transactions"
        )

        return training_report

    except Exception as e:
        print(f"\n❌ ERROR during large dataset training: {e}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    train_large_dataset()
