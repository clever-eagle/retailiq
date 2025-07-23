import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from collections import defaultdict, Counter


class MarketBasketAnalyzer:
    """
    Market Basket Analysis using Apriori Algorithm
    Finds frequent itemsets and association rules
    """

    def __init__(self):
        self.frequent_itemsets = None
        self.association_rules = None
        self.transaction_encoder = TransactionEncoder()

    def prepare_transactions(self, df):
        """
        Prepare transaction data for Apriori analysis
        Convert DataFrame to list of transactions
        """
        try:
            # Group by transaction_id and collect products
            transactions = (
                df.groupby("transaction_id")["product_name"].apply(list).tolist()
            )

            # Alternative: Group by customer_id and date for session-based analysis
            # df['session'] = df['customer_id'].astype(str) + '_' + df['date'].astype(str)
            # transactions = df.groupby('session')['product_name'].apply(list).tolist()

            return transactions
        except Exception as e:
            print(f"Error preparing transactions: {e}")
            return []

    def get_frequent_itemsets(self, df, min_support=0.01):
        """
        Find frequent itemsets using Apriori algorithm
        """
        try:
            transactions = self.prepare_transactions(df)
            if not transactions:
                return []

            # Convert transactions to one-hot encoded format
            te_ary = self.transaction_encoder.fit(transactions).transform(transactions)
            transaction_df = pd.DataFrame(
                te_ary, columns=self.transaction_encoder.columns_
            )

            # Apply Apriori algorithm with lower minimum support for synthetic data
            frequent_itemsets = apriori(
                transaction_df,
                min_support=0.001,
                use_colnames=True,  # Lowered from default
            )

            if frequent_itemsets.empty:
                return []

            # Convert frozensets to lists for JSON serialization
            frequent_itemsets["itemsets"] = frequent_itemsets["itemsets"].apply(
                lambda x: list(x)
            )

            # Sort by support in descending order
            frequent_itemsets = frequent_itemsets.sort_values(
                "support", ascending=False
            )

            self.frequent_itemsets = frequent_itemsets

            return frequent_itemsets.to_dict("records")

        except Exception as e:
            print(f"Error in frequent itemsets analysis: {e}")
            return []

    def generate_association_rules(
        self, df, min_support=0.01, min_confidence=0.2, min_lift=1.0
    ):
        """
        Generate association rules from frequent itemsets
        """
        try:
            transactions = self.prepare_transactions(df)
            if not transactions:
                return []

            # Get frequent itemsets first
            te_ary = self.transaction_encoder.fit(transactions).transform(transactions)
            transaction_df = pd.DataFrame(
                te_ary, columns=self.transaction_encoder.columns_
            )

            frequent_itemsets = apriori(
                transaction_df, min_support=min_support, use_colnames=True
            )

            if frequent_itemsets.empty:
                return []

            # Generate association rules
            rules = association_rules(
                frequent_itemsets, metric="confidence", min_threshold=min_confidence
            )

            if rules.empty:
                return []

            # Filter by lift
            rules = rules[rules["lift"] >= min_lift]

            if rules.empty:
                return []

            # Convert frozensets to lists for JSON serialization
            rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x))
            rules["consequents"] = rules["consequents"].apply(lambda x: list(x))

            # Sort by confidence and lift
            rules = rules.sort_values(["confidence", "lift"], ascending=False)

            self.association_rules = rules

            # Select relevant columns for output
            output_rules = rules[
                ["antecedents", "consequents", "support", "confidence", "lift"]
            ].copy()

            return output_rules.to_dict("records")

        except Exception as e:
            print(f"Error generating association rules: {e}")
            return []

    def get_recommendations(self, df, current_items, top_n=5):
        """
        Get product recommendations based on current items using association rules
        """
        try:
            # First generate association rules if not already done
            if self.association_rules is None:
                self.generate_association_rules(df)

            if self.association_rules is None or self.association_rules.empty:
                return self._get_popularity_based_recommendations(
                    df, current_items, top_n
                )

            recommendations = []
            current_items_set = set(current_items)

            # Find rules where antecedents are subset of current items
            for _, rule in self.association_rules.iterrows():
                antecedents_set = set(rule["antecedents"])
                consequents_set = set(rule["consequents"])

                # Check if antecedents are subset of current items
                if antecedents_set.issubset(current_items_set):
                    # Add consequents that are not already in current items
                    for item in consequents_set:
                        if item not in current_items_set:
                            recommendations.append(
                                {
                                    "product": item,
                                    "confidence": float(rule["confidence"]),
                                    "lift": float(rule["lift"]),
                                    "support": float(rule["support"]),
                                    "based_on": list(antecedents_set),
                                }
                            )

            # Sort by confidence and lift
            recommendations.sort(
                key=lambda x: (x["confidence"], x["lift"]), reverse=True
            )

            # Remove duplicates while preserving order
            seen = set()
            unique_recommendations = []
            for rec in recommendations:
                if rec["product"] not in seen:
                    seen.add(rec["product"])
                    unique_recommendations.append(rec)

            # Return top N recommendations
            return unique_recommendations[:top_n]

        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return self._get_popularity_based_recommendations(df, current_items, top_n)

    def _get_popularity_based_recommendations(self, df, current_items, top_n=5):
        """
        Fallback to popularity-based recommendations if association rules fail
        """
        try:
            current_items_set = set(current_items)

            # Get product popularity (frequency)
            product_counts = df["product_name"].value_counts()

            recommendations = []
            for product, count in product_counts.items():
                if product not in current_items_set:
                    recommendations.append(
                        {
                            "product": product,
                            "confidence": 0.0,
                            "lift": 0.0,
                            "support": count / len(df),
                            "based_on": ["popularity"],
                        }
                    )

            return recommendations[:top_n]

        except Exception as e:
            print(f"Error in popularity-based recommendations: {e}")
            return []

    def analyze(self, df, min_support=0.01, min_confidence=0.2, min_lift=1.0):
        """
        Perform complete market basket analysis
        """
        try:
            # Get frequent itemsets
            frequent_itemsets = self.get_frequent_itemsets(df, min_support)

            # Generate association rules
            association_rules = self.generate_association_rules(
                df, min_support, min_confidence, min_lift
            )

            # Get basic statistics
            total_transactions = df["transaction_id"].nunique()
            total_products = df["product_name"].nunique()
            avg_items_per_transaction = df.groupby("transaction_id").size().mean()

            return {
                "frequent_itemsets": frequent_itemsets,
                "association_rules": association_rules,
                "statistics": {
                    "total_transactions": int(total_transactions),
                    "total_products": int(total_products),
                    "avg_items_per_transaction": float(avg_items_per_transaction),
                    "min_support": min_support,
                    "min_confidence": min_confidence,
                    "min_lift": min_lift,
                },
            }

        except Exception as e:
            print(f"Error in market basket analysis: {e}")
            return {
                "frequent_itemsets": [],
                "association_rules": [],
                "statistics": {},
                "error": str(e),
            }
