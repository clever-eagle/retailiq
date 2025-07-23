"""
Market Basket Analysis using Apriori Algorithm - Built from Scratch
This module implements the Apriori algorithm for finding frequent itemsets
and generating association rules for market basket analysis.
"""

import pandas as pd
import numpy as np
from collections import defaultdict, Counter
from itertools import combinations
import json


class AprioriAnalyzer:
    """
    Complete implementation of Apriori algorithm for market basket analysis
    """
    
    def __init__(self):
        self.transactions = []
        self.frequent_itemsets = {}
        self.association_rules = []
        self.item_support = {}
        
    def load_transactions(self, df):
        """
        Load and prepare transaction data
        Expected columns: transaction_id, product_name
        """
        try:
            # Group products by transaction
            transactions = df.groupby('transaction_id')['product_name'].apply(list).tolist()
            
            # Convert to sets for faster operations
            self.transactions = [set(transaction) for transaction in transactions]
            
            print(f"Loaded {len(self.transactions)} transactions")
            print(f"Sample transaction: {list(self.transactions[0]) if self.transactions else 'None'}")
            
            return True
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return False
    
    def get_item_support(self, itemset):
        """
        Calculate support for a given itemset
        Support = count of transactions containing itemset / total transactions
        """
        if not self.transactions:
            return 0
            
        count = sum(1 for transaction in self.transactions if itemset.issubset(transaction))
        return count / len(self.transactions)
    
    def find_frequent_1_itemsets(self, min_support):
        """
        Find all frequent 1-itemsets (single items)
        """
        # Count frequency of each item
        item_counts = Counter()
        for transaction in self.transactions:
            for item in transaction:
                item_counts[item] += 1
        
        # Calculate support and filter by minimum support
        frequent_items = set()
        self.item_support = {}
        
        for item, count in item_counts.items():
            support = count / len(self.transactions)
            self.item_support[item] = support
            
            if support >= min_support:
                frequent_items.add(frozenset([item]))
        
        print(f"Found {len(frequent_items)} frequent 1-itemsets")
        return frequent_items
    
    def generate_candidates(self, frequent_itemsets, k):
        """
        Generate candidate k-itemsets from frequent (k-1)-itemsets
        """
        candidates = set()
        frequent_list = list(frequent_itemsets)
        
        for i in range(len(frequent_list)):
            for j in range(i + 1, len(frequent_list)):
                # Join step: union of two frequent (k-1)-itemsets
                candidate = frequent_list[i] | frequent_list[j]
                
                # Only consider if the union has exactly k items
                if len(candidate) == k:
                    # Prune step: check if all (k-1)-subsets are frequent
                    is_valid = True
                    for item in candidate:
                        subset = candidate - frozenset([item])
                        if subset not in frequent_itemsets:
                            is_valid = False
                            break
                    
                    if is_valid:
                        candidates.add(candidate)
        
        return candidates
    
    def find_frequent_itemsets(self, min_support=0.01):
        """
        Main Apriori algorithm to find all frequent itemsets
        """
        print(f"Starting Apriori with min_support = {min_support}")
        
        if not self.transactions:
            print("No transactions loaded")
            return {}
        
        all_frequent_itemsets = {}
        
        # Find frequent 1-itemsets
        frequent_1_itemsets = self.find_frequent_1_itemsets(min_support)
        if not frequent_1_itemsets:
            print("No frequent 1-itemsets found")
            return {}
        
        all_frequent_itemsets[1] = frequent_1_itemsets
        k = 2
        
        # Iteratively find frequent k-itemsets
        while True:
            # Generate candidates
            candidates = self.generate_candidates(all_frequent_itemsets[k-1], k)
            
            if not candidates:
                break
            
            # Test candidates and find frequent k-itemsets
            frequent_k_itemsets = set()
            for candidate in candidates:
                support = self.get_item_support(candidate)
                if support >= min_support:
                    frequent_k_itemsets.add(candidate)
            
            if not frequent_k_itemsets:
                break
            
            all_frequent_itemsets[k] = frequent_k_itemsets
            print(f"Found {len(frequent_k_itemsets)} frequent {k}-itemsets")
            k += 1
        
        self.frequent_itemsets = all_frequent_itemsets
        return all_frequent_itemsets
    
    def generate_association_rules(self, min_confidence=0.5, min_lift=1.0):
        """
        Generate association rules from frequent itemsets
        """
        rules = []
        
        # Generate rules from itemsets of size 2 and above
        for k in range(2, max(self.frequent_itemsets.keys()) + 1):
            for itemset in self.frequent_itemsets[k]:
                itemset_support = self.get_item_support(itemset)
                
                # Generate all possible antecedent/consequent combinations
                for i in range(1, len(itemset)):
                    for antecedent in combinations(itemset, i):
                        antecedent = frozenset(antecedent)
                        consequent = itemset - antecedent
                        
                        # Calculate confidence
                        antecedent_support = self.get_item_support(antecedent)
                        if antecedent_support == 0:
                            continue
                            
                        confidence = itemset_support / antecedent_support
                        
                        # Calculate lift
                        consequent_support = self.get_item_support(consequent)
                        if consequent_support == 0:
                            continue
                            
                        lift = confidence / consequent_support
                        
                        # Filter by thresholds
                        if confidence >= min_confidence and lift >= min_lift:
                            # Calculate conviction
                            conviction = (1 - consequent_support) / (1 - confidence) if confidence < 1 else float('inf')
                            
                            rule = {
                                'antecedents': list(antecedent),
                                'consequents': list(consequent),
                                'support': round(itemset_support, 4),
                                'confidence': round(confidence, 4),
                                'lift': round(lift, 4),
                                'conviction': round(conviction, 4),
                                'transaction_count': int(itemset_support * len(self.transactions))
                            }
                            rules.append(rule)
        
        # Sort rules by confidence and lift
        rules.sort(key=lambda x: (x['confidence'], x['lift']), reverse=True)
        
        self.association_rules = rules
        print(f"Generated {len(rules)} association rules")
        return rules
    
    def get_formatted_frequent_itemsets(self):
        """
        Get frequent itemsets in a formatted structure for API response
        """
        formatted_itemsets = []
        
        for k, itemsets in self.frequent_itemsets.items():
            for itemset in itemsets:
                support = self.get_item_support(itemset)
                formatted_itemsets.append({
                    'itemsets': list(itemset),
                    'support': round(support, 4),
                    'size': len(itemset),
                    'transaction_count': int(support * len(self.transactions))
                })
        
        # Sort by support (descending)
        formatted_itemsets.sort(key=lambda x: x['support'], reverse=True)
        return formatted_itemsets
    
    def get_recommendations(self, current_items, top_n=5):
        """
        Get product recommendations based on current items using association rules
        """
        recommendations = []
        current_items_set = set(current_items)
        
        for rule in self.association_rules:
            antecedents_set = set(rule['antecedents'])
            
            # Check if current items contain the antecedents
            if antecedents_set.issubset(current_items_set):
                for consequent in rule['consequents']:
                    if consequent not in current_items_set:
                        recommendations.append({
                            'product': consequent,
                            'confidence': rule['confidence'],
                            'lift': rule['lift'],
                            'rule_antecedents': rule['antecedents'],
                            'support': rule['support']
                        })
        
        # Remove duplicates and sort by confidence
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['product'] not in seen:
                seen.add(rec['product'])
                unique_recommendations.append(rec)
        
        unique_recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        return unique_recommendations[:top_n]
    
    def analyze(self, df, min_support=0.01, min_confidence=0.5, min_lift=1.0):
        """
        Complete market basket analysis
        """
        try:
            print("=== Starting Market Basket Analysis ===")
            print(f"Dataset shape: {df.shape}")
            print(f"Parameters: min_support={min_support}, min_confidence={min_confidence}, min_lift={min_lift}")
            
            # Load transactions
            if not self.load_transactions(df):
                raise Exception("Failed to load transactions")
            
            # Find frequent itemsets
            frequent_itemsets = self.find_frequent_itemsets(min_support)
            if not frequent_itemsets:
                raise Exception("No frequent itemsets found with the given support threshold")
            
            # Generate association rules
            association_rules = self.generate_association_rules(min_confidence, min_lift)
            
            # Get formatted results
            formatted_itemsets = self.get_formatted_frequent_itemsets()
            
            # Calculate statistics
            total_transactions = len(self.transactions)
            total_unique_items = len(set().union(*self.transactions)) if self.transactions else 0
            avg_items_per_transaction = np.mean([len(t) for t in self.transactions]) if self.transactions else 0
            
            results = {
                'frequent_itemsets': formatted_itemsets,
                'association_rules': association_rules,
                'statistics': {
                    'total_transactions': total_transactions,
                    'total_unique_items': total_unique_items,
                    'avg_items_per_transaction': round(avg_items_per_transaction, 2),
                    'frequent_itemsets_count': len(formatted_itemsets),
                    'association_rules_count': len(association_rules),
                    'min_support': min_support,
                    'min_confidence': min_confidence,
                    'min_lift': min_lift
                },
                'success': True
            }
            
            print("=== Analysis Complete ===")
            print(f"Found {len(formatted_itemsets)} frequent itemsets")
            print(f"Generated {len(association_rules)} association rules")
            
            return results
            
        except Exception as e:
            print(f"Error in market basket analysis: {e}")
            return {
                'frequent_itemsets': [],
                'association_rules': [],
                'statistics': {},
                'error': str(e),
                'success': False
            }


# Test function for development
def test_apriori():
    """
    Test the Apriori analyzer with sample data
    """
    # Create sample transaction data
    sample_data = {
        'transaction_id': [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6],
        'product_name': ['Bread', 'Milk', 'Butter', 'Bread', 'Milk', 'Bread', 'Butter', 'Cheese', 
                        'Milk', 'Cheese', 'Bread', 'Milk', 'Butter', 'Beer', 'Chips']
    }
    
    df = pd.DataFrame(sample_data)
    
    analyzer = AprioriAnalyzer()
    results = analyzer.analyze(df, min_support=0.3, min_confidence=0.5, min_lift=1.0)
    
    print("\n=== TEST RESULTS ===")
    print(json.dumps(results, indent=2))
    
    return results


if __name__ == "__main__":
    test_apriori()
