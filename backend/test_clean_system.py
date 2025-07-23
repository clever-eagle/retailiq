#!/usr/bin/env python3
"""
Test script to demonstrate the clean CSV analysis system
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def test_empty_state():
    """Test that system starts empty"""
    print("🧪 Testing empty state...")

    response = requests.get(f"{BASE_URL}/data-summary")
    data = response.json()

    print(f"✅ Empty state: {data.get('message', 'No message')}")
    print(f"📊 Has data: {data.get('has_data', False)}")


def test_csv_upload():
    """Test CSV upload and analysis"""
    print("\n🧪 Testing CSV upload...")

    # Upload a CSV file
    with open("large_market_basket_data.csv", "rb") as f:
        files = {"file": f}
        response = requests.post(f"{BASE_URL}/upload-data", files=files)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload successful: {data.get('message', 'No message')}")
        print(f"📁 File: {data.get('file_info', {}).get('filename', 'Unknown')}")
        print(f"📊 Records: {data.get('file_info', {}).get('records', 0)}")

        # Check data summary after upload
        response = requests.get(f"{BASE_URL}/data-summary")
        summary_data = response.json()
        print(
            f"📈 Revenue: ${summary_data.get('analysis', {}).get('revenue', {}).get('total_revenue', 0):,.2f}"
        )
        print(
            f"👥 Customers: {summary_data.get('analysis', {}).get('transactions', {}).get('total_customers', 0)}"
        )
    else:
        print(f"❌ Upload failed: {response.text}")


def test_current_analysis():
    """Test getting current analysis"""
    print("\n🧪 Testing current analysis...")

    response = requests.get(f"{BASE_URL}/current-analysis")
    data = response.json()

    print(f"📊 Has analysis: {data.get('has_analysis', False)}")
    if data.get("has_analysis"):
        print(
            f"📁 Last file: {data.get('analysis', {}).get('file_info', {}).get('filename', 'Unknown')}"
        )
        print(f"⏰ Last updated: {data.get('last_updated', 'Unknown')}")


if __name__ == "__main__":
    print("🎯 Testing Clean CSV Analysis System")
    print("=" * 50)

    try:
        # Test empty state
        test_empty_state()

        # Test CSV upload
        test_csv_upload()

        # Test current analysis
        test_current_analysis()

        print("\n✅ All tests completed!")

    except requests.exceptions.ConnectionError:
        print(
            "❌ Cannot connect to server. Make sure Flask app is running on localhost:5000"
        )
    except Exception as e:
        print(f"❌ Test failed: {e}")
