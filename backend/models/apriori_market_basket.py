import pandas as pd
import numpy as np
from itertools import combinations
from collections import defaultdict, Counter
import json
import time


class AprioriMarketBasket:
    """
    Enhanced Market Basket Analysis implementation using Apriori Algorithm
    Optimized for large datasets with performance monitoring
    """

    def __init__(self):
        self.transactions = []
        self.frequent_itemsets = {}
        self.association_rules = []
        self.item_support = {}
        self.performance_stats = {}

    def load_transactions(self, df):
        """
        Load and prepare transaction data from DataFrame with performance optimization
        """
        try:
            start_time = time.time()
            print(f"Loading transactions from DataFrame with {len(df)} rows")

            # Group by transaction_id to get items per transaction
            self.transactions = []
            transaction_groups = df.groupby("transaction_id")["product_name"].apply(
                list
            )

            for transaction_id, items in transaction_groups.items():
                # Remove duplicates and convert to set for faster operations
                unique_items = list(set(items))
                if len(unique_items) > 0:  # Only include non-empty transactions
                    self.transactions.append(unique_items)

            load_time = time.time() - start_time

            print(
                f"Prepared {len(self.transactions)} unique transactions in {load_time:.2f}s"
            )
            print(
                f"Average items per transaction: {np.mean([len(t) for t in self.transactions]):.2f}"
            )
            print(
                f"Sample transaction: {self.transactions[0] if self.transactions else 'None'}"
            )

            # Store performance stats
            self.performance_stats["load_time"] = load_time
            self.performance_stats["total_transactions"] = len(self.transactions)
            self.performance_stats["avg_items_per_transaction"] = np.mean(
                [len(t) for t in self.transactions]
            )

            return len(self.transactions)

        except Exception as e:
            print(f"Error loading transactions: {e}")
            return 0

    def calculate_support(self, itemset):
        """
        Calculate support for a given itemset
        Support = Number of transactions containing itemset / Total transactions
        """
        if not self.transactions:
            return 0

        count = 0
        for transaction in self.transactions:
            if set(itemset).issubset(set(transaction)):
                count += 1

        return count / len(self.transactions)

    def get_frequent_1_itemsets(self, min_support):
        """
        Get frequent 1-itemsets (individual items) with optimization
        """
        start_time = time.time()

        # Count frequency of each item
        item_counts = defaultdict(int)

        for transaction in self.transactions:
            for item in transaction:
                item_counts[item] += 1

        # Calculate support and filter
        frequent_1_itemsets = []
        total_transactions = len(self.transactions)

        for item, count in item_counts.items():
            support = count / total_transactions
            if support >= min_support:
                frequent_1_itemsets.append([item])
                self.item_support[item] = support

        processing_time = time.time() - start_time
        print(
            f"Found {len(frequent_1_itemsets)} frequent 1-itemsets in {processing_time:.2f}s"
        )
        print(
            f"Top 10 items by support: {sorted(self.item_support.items(), key=lambda x: x[1], reverse=True)[:10]}"
        )

        return frequent_1_itemsets

    def generate_candidate_itemsets(self, frequent_itemsets, k):
        """
        Generate candidate k-itemsets from frequent (k-1)-itemsets
        """
        candidates = []
        n = len(frequent_itemsets)

        for i in range(n):
            for j in range(i + 1, n):
                # Join two (k-1)-itemsets if they differ by only one item
                set1 = set(frequent_itemsets[i])
                set2 = set(frequent_itemsets[j])

                # Union of the two sets
                union = set1.union(set2)

                if len(union) == k:
                    candidate = sorted(list(union))
                    if candidate not in candidates:
                        candidates.append(candidate)

        return candidates

    def prune_candidates(self, candidates, frequent_prev):
        """
        Prune candidates that have infrequent subsets
        """
        pruned = []
        frequent_prev_set = [set(itemset) for itemset in frequent_prev]

        for candidate in candidates:
            # Check if all (k-1)-subsets are frequent
            is_valid = True
            for i in range(len(candidate)):
                subset = candidate[:i] + candidate[i + 1 :]
                if set(subset) not in frequent_prev_set:
                    is_valid = False
                    break

            if is_valid:
                pruned.append(candidate)

        return pruned

    def find_frequent_itemsets(self, min_support=0.01):
        """
        Find all frequent itemsets using Apriori algorithm
        """
        print(f"Finding frequent itemsets with min_support={min_support}")

        if not self.transactions:
            print("No transactions loaded")
            return {}

        self.frequent_itemsets = {}

        # Find frequent 1-itemsets
        frequent_1 = self.get_frequent_1_itemsets(min_support)
        if not frequent_1:
            print("No frequent 1-itemsets found")
            return {}

        self.frequent_itemsets[1] = frequent_1
        print(f"Frequent 1-itemsets: {frequent_1[:5]}...")  # Show first 5

        k = 2
        frequent_prev = frequent_1

        while frequent_prev:
            print(f"Finding frequent {k}-itemsets...")

            # Generate candidates
            candidates = self.generate_candidate_itemsets(frequent_prev, k)
            print(f"Generated {len(candidates)} candidates")

            if not candidates:
                break

            # Prune candidates
            if k > 2:
                candidates = self.prune_candidates(candidates, frequent_prev)
                print(f"After pruning: {len(candidates)} candidates")

            # Check support for each candidate
            frequent_k = []
            for candidate in candidates:
                support = self.calculate_support(candidate)
                if support >= min_support:
                    frequent_k.append(candidate)

            print(f"Found {len(frequent_k)} frequent {k}-itemsets")

            if frequent_k:
                self.frequent_itemsets[k] = frequent_k
                frequent_prev = frequent_k
                k += 1
            else:
                break

        return self.frequent_itemsets

    def generate_association_rules(self, min_confidence=0.2, min_lift=1.0):
        """
        Generate association rules from frequent itemsets
        """
        print(
            f"Generating association rules with min_confidence={min_confidence}, min_lift={min_lift}"
        )

        self.association_rules = []

        # Only generate rules from itemsets of size 2 or more
        for k in range(2, max(self.frequent_itemsets.keys()) + 1):
            if k not in self.frequent_itemsets:
                continue

            for itemset in self.frequent_itemsets[k]:
                # Generate all possible antecedent-consequent combinations
                for i in range(1, len(itemset)):
                    for antecedent in combinations(itemset, i):
                        antecedent = list(antecedent)
                        consequent = [
                            item for item in itemset if item not in antecedent
                        ]

                        # Calculate metrics
                        itemset_support = self.calculate_support(itemset)
                        antecedent_support = self.calculate_support(antecedent)
                        consequent_support = self.calculate_support(consequent)

                        if antecedent_support == 0:
                            continue

                        confidence = itemset_support / antecedent_support

                        if consequent_support == 0:
                            lift = 0
                        else:
                            lift = confidence / consequent_support

                        # Check thresholds
                        if confidence >= min_confidence and lift >= min_lift:
                            rule = {
                                "antecedent": antecedent,
                                "consequent": consequent,
                                "support": round(itemset_support, 4),
                                "confidence": round(confidence, 4),
                                "lift": round(lift, 4),
                                "antecedent_support": round(antecedent_support, 4),
                                "consequent_support": round(consequent_support, 4),
                            }
                            self.association_rules.append(rule)

        # Sort by confidence and lift
        self.association_rules.sort(
            key=lambda x: (x["confidence"], x["lift"]), reverse=True
        )

        print(f"Generated {len(self.association_rules)} association rules")
        return self.association_rules

    def get_recommendations(self, current_items, top_n=5):
        """
        Get product recommendations based on current items
        """
        recommendations = []

        for rule in self.association_rules:
            # Check if current items contain the antecedent
            if set(rule["antecedent"]).issubset(set(current_items)):
                # Check if consequent items are not already in current items
                new_items = [
                    item for item in rule["consequent"] if item not in current_items
                ]
                if new_items:
                    for item in new_items:
                        recommendations.append(
                            {
                                "product": item,
                                "confidence": rule["confidence"],
                                "lift": rule["lift"],
                                "support": rule["support"],
                                "reason": f"Customers who bought {', '.join(rule['antecedent'])} also bought this",
                            }
                        )

        # Remove duplicates and sort by confidence
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec["product"] not in seen:
                seen.add(rec["product"])
                unique_recommendations.append(rec)

        unique_recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        return unique_recommendations[:top_n]

    def analyze(self, df, min_support=0.01, min_confidence=0.2, min_lift=1.0):
        """
        Complete market basket analysis with enhanced analytics
        """
        try:
            overall_start_time = time.time()
            print("Starting enhanced market basket analysis...")
            print(
                f"Parameters: min_support={min_support}, min_confidence={min_confidence}, min_lift={min_lift}"
            )

            # Load transactions
            num_transactions = self.load_transactions(df)
            if num_transactions == 0:
                return {
                    "error": "No valid transactions found",
                    "frequent_itemsets": {},
                    "association_rules": [],
                    "statistics": {},
                }

            # Find frequent itemsets
            frequent_itemsets = self.find_frequent_itemsets(min_support)

            # Generate association rules
            association_rules = self.generate_association_rules(
                min_confidence, min_lift
            )

            # Calculate comprehensive statistics
            total_items = len(
                set([item for transaction in self.transactions for item in transaction])
            )
            avg_items_per_transaction = sum(len(t) for t in self.transactions) / len(
                self.transactions
            )

            # Advanced analytics
            total_analysis_time = time.time() - overall_start_time

            # Category analysis (if category data available)
            category_stats = self._analyze_categories(df)

            # Customer persona analysis (if persona data available)
            persona_stats = self._analyze_personas(df)

            # Seasonal patterns (if date data available)
            temporal_stats = self._analyze_temporal_patterns(df)

            # Format frequent itemsets for JSON response
            formatted_itemsets = {}
            for k, itemsets in frequent_itemsets.items():
                formatted_itemsets[str(k)] = [
                    {
                        "itemset": itemset,
                        "support": round(self.calculate_support(itemset), 4),
                        "frequency": int(
                            self.calculate_support(itemset) * num_transactions
                        ),
                    }
                    for itemset in itemsets
                ]

            result = {
                "frequent_itemsets": formatted_itemsets,
                "association_rules": association_rules,
                "statistics": {
                    "total_transactions": num_transactions,
                    "total_unique_items": total_items,
                    "avg_items_per_transaction": round(avg_items_per_transaction, 2),
                    "total_rules_generated": len(association_rules),
                    "analysis_time_seconds": round(total_analysis_time, 2),
                    "strong_rules": len(
                        [r for r in association_rules if r["lift"] > 2.0]
                    ),
                    "very_strong_rules": len(
                        [r for r in association_rules if r["lift"] > 3.0]
                    ),
                    "dataset_size": (
                        "Large"
                        if num_transactions > 10000
                        else "Medium" if num_transactions > 1000 else "Small"
                    ),
                    "performance": self.performance_stats,
                    "min_support": min_support,
                    "min_confidence": min_confidence,
                    "min_lift": min_lift,
                    "frequent_itemsets_count": sum(
                        len(itemsets) for itemsets in frequent_itemsets.values()
                    ),
                    "association_rules_count": len(association_rules),
                },
                "advanced_analytics": {
                    "category_insights": category_stats,
                    "persona_insights": persona_stats,
                    "temporal_patterns": temporal_stats,
                },
            }

            print("Market basket analysis completed successfully!")
            print(f"Found {len(association_rules)} association rules")

            return result

        except Exception as e:
            print(f"Error in market basket analysis: {e}")
            import traceback

            traceback.print_exc()
            return {
                "error": str(e),
                "frequent_itemsets": {},
                "association_rules": [],
                "statistics": {},
            }

    def _analyze_categories(self, df):
        """
        Analyze product categories for insights
        """
        try:
            if "category" not in df.columns:
                return {"message": "No category data available"}

            category_counts = df["category"].value_counts()
            total_items = len(df)

            category_insights = {
                "top_categories": [
                    {
                        "category": cat,
                        "count": int(count),
                        "percentage": round((count / total_items) * 100, 2),
                    }
                    for cat, count in category_counts.head(10).items()
                ],
                "total_categories": len(category_counts),
                "category_distribution": category_counts.to_dict(),
            }

            return category_insights
        except Exception as e:
            return {"error": f"Category analysis failed: {str(e)}"}

    def _analyze_personas(self, df):
        """
        Analyze customer personas for insights
        """
        try:
            if "persona" not in df.columns:
                return {"message": "No persona data available"}

            persona_counts = df["persona"].value_counts()
            total_transactions = len(df["transaction_id"].unique())

            # Calculate average items per persona
            persona_stats = (
                df.groupby("persona")
                .agg({"transaction_id": "nunique", "product_name": "count"})
                .reset_index()
            )

            persona_stats["avg_items_per_transaction"] = (
                persona_stats["product_name"] / persona_stats["transaction_id"]
            ).round(2)

            persona_insights = {
                "persona_distribution": [
                    {
                        "persona": row["persona"],
                        "transactions": int(row["transaction_id"]),
                        "total_items": int(row["product_name"]),
                        "avg_items_per_transaction": float(
                            row["avg_items_per_transaction"]
                        ),
                        "market_share": round(
                            (row["transaction_id"] / total_transactions) * 100, 2
                        ),
                    }
                    for _, row in persona_stats.iterrows()
                ],
                "total_personas": len(persona_counts),
            }

            return persona_insights
        except Exception as e:
            return {"error": f"Persona analysis failed: {str(e)}"}

    def _analyze_temporal_patterns(self, df):
        """
        Analyze temporal purchasing patterns
        """
        try:
            if "date" not in df.columns:
                return {"message": "No date data available"}

            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.month
            df["day_of_week"] = df["date"].dt.day_name()
            df["quarter"] = df["date"].dt.quarter

            monthly_patterns = df.groupby("month")["transaction_id"].nunique().to_dict()
            weekly_patterns = (
                df.groupby("day_of_week")["transaction_id"].nunique().to_dict()
            )
            quarterly_patterns = (
                df.groupby("quarter")["transaction_id"].nunique().to_dict()
            )

            temporal_insights = {
                "monthly_transactions": monthly_patterns,
                "weekly_patterns": weekly_patterns,
                "quarterly_patterns": quarterly_patterns,
                "date_range": {
                    "start": df["date"].min().strftime("%Y-%m-%d"),
                    "end": df["date"].max().strftime("%Y-%m-%d"),
                    "days_covered": (df["date"].max() - df["date"].min()).days,
                },
            }

            return temporal_insights
        except Exception as e:
            return {"error": f"Temporal analysis failed: {str(e)}"}
