#!/usr/bin/env python3
"""
Test script for the Retail Analytics Backend
Run this to test API endpoints
"""

import requests
import json
import pandas as pd
from datetime import datetime
import time

BASE_URL = "http://localhost:5000"


def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running.")
        return False


def test_data_summary():
    """Test data summary endpoint"""
    print("\n🔍 Testing data summary endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/data-summary")
        if response.status_code == 200:
            data = response.json()
            print("✅ Data summary retrieved successfully")
            print(
                f"   📊 Total transactions: {data['data']['transactions']['total_transactions']}"
            )
            print(f"   🛍️ Total products: {data['data']['products']['total_products']}")
            return True
        else:
            print(f"❌ Data summary failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Data summary error: {e}")
        return False


def test_market_basket_analysis():
    """Test market basket analysis endpoint"""
    print("\n🔍 Testing market basket analysis...")
    try:
        payload = {"min_support": 0.01, "min_confidence": 0.2, "min_lift": 1.0}
        response = requests.post(
            f"{BASE_URL}/market-basket-analysis",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Market basket analysis completed")

            frequent_itemsets = data["data"]["frequent_itemsets"]
            association_rules = data["data"]["association_rules"]

            print(f"   📈 Found {len(frequent_itemsets)} frequent itemsets")
            print(f"   🔗 Found {len(association_rules)} association rules")

            if association_rules:
                best_rule = association_rules[0]
                print(
                    f"   🏆 Best rule: {best_rule['antecedents']} → {best_rule['consequents']}"
                )
                print(
                    f"      Confidence: {best_rule['confidence']:.3f}, Lift: {best_rule['lift']:.3f}"
                )

            return True
        else:
            print(f"❌ Market basket analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Market basket analysis error: {e}")
        return False


def test_recommendations():
    """Test product recommendations endpoint"""
    print("\n🔍 Testing product recommendations...")
    try:
        payload = {"items": ["Coffee", "Laptop"]}
        response = requests.post(
            f"{BASE_URL}/get-recommendations",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Product recommendations retrieved")

            recommendations = data["data"]["recommendations"]
            print(f"   💡 Found {len(recommendations)} recommendations")

            for i, rec in enumerate(recommendations[:3], 1):
                print(f"   {i}. {rec['product']} (confidence: {rec['confidence']:.3f})")

            return True
        else:
            print(f"❌ Recommendations failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Recommendations error: {e}")
        return False


def test_sales_forecast():
    """Test sales forecasting endpoint"""
    print("\n🔍 Testing sales forecasting...")
    try:
        payload = {"forecast_days": 7}
        response = requests.post(
            f"{BASE_URL}/sales-forecast",
            json=payload,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Sales forecast generated")

            forecasts = data["data"]["forecasts"]
            print(f"   📊 Available forecast models: {list(forecasts.keys())}")

            if "ensemble" in forecasts:
                ensemble_forecast = forecasts["ensemble"]
                if ensemble_forecast:
                    avg_prediction = sum(
                        f["predicted_revenue"] for f in ensemble_forecast
                    ) / len(ensemble_forecast)
                    print(
                        f"   💰 Average daily revenue prediction: ${avg_prediction:.2f}"
                    )

            return True
        else:
            print(f"❌ Sales forecast failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Sales forecast error: {e}")
        return False


def test_sales_trends():
    """Test sales trends endpoint"""
    print("\n🔍 Testing sales trends...")
    try:
        response = requests.get(f"{BASE_URL}/sales-trends")

        if response.status_code == 200:
            data = response.json()
            print("✅ Sales trends retrieved")

            summary = data["data"]["summary"]
            print(f"   💰 Total revenue: ${summary['total_revenue']:.2f}")
            print(f"   📅 Average daily revenue: ${summary['avg_daily_revenue']:.2f}")
            print(f"   📈 Revenue growth rate: {summary['revenue_growth_rate']:.2f}%")

            return True
        else:
            print(f"❌ Sales trends failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Sales trends error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("🧪 Starting Backend API Tests")
    print("=" * 50)

    tests = [
        ("Health Check", test_health),
        ("Data Summary", test_data_summary),
        ("Market Basket Analysis", test_market_basket_analysis),
        ("Product Recommendations", test_recommendations),
        ("Sales Forecasting", test_sales_forecast),
        ("Sales Trends", test_sales_trends),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        result = test_func()
        if result:
            passed += 1
        time.sleep(0.5)  # Small delay between tests

    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

    return passed == total


if __name__ == "__main__":
    run_all_tests()
