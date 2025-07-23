"""
Auto Data Upload Script
Automatically uploads training data to the backend for immediate testing
"""

import requests
import pandas as pd
import os


def upload_training_data():
    """Upload the training data to the backend"""

    # Backend URL
    backend_url = "http://localhost:5000"

    # Path to training data
    training_data_path = os.path.join(os.path.dirname(__file__), "training_data.csv")

    if not os.path.exists(training_data_path):
        print("❌ Training data not found. Please run train_models.py first.")
        return False

    try:
        # Read and prepare the data
        print("📤 Uploading training data to backend...")

        # Upload the CSV file
        with open(training_data_path, "rb") as f:
            files = {"file": ("training_data.csv", f, "text/csv")}
            response = requests.post(f"{backend_url}/upload-data", files=files)

        if response.status_code == 200:
            result = response.json()
            print("✅ Training data uploaded successfully!")
            print(f"   - Uploaded {result.get('total_records', 'unknown')} records")
            print(f"   - Data processed and ready for analysis")
            return True
        else:
            print(f"❌ Upload failed: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error uploading data: {str(e)}")
        return False


def test_api_endpoints():
    """Test that all API endpoints are working"""

    backend_url = "http://localhost:5000"

    print("\n🧪 Testing API endpoints...")

    # Test health check
    try:
        response = requests.get(f"{backend_url}/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
        else:
            print("❌ Health check: Failed")
    except:
        print("❌ Health check: Backend not responding")
        return False

    # Test market basket analysis
    try:
        test_data = {"current_items": ["Coffee Maker", "Coffee Beans"]}
        response = requests.post(f"{backend_url}/get-recommendations", json=test_data)
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ Market basket analysis: {len(recommendations)} recommendations")
        else:
            print("❌ Market basket analysis: Failed")
    except Exception as e:
        print(f"❌ Market basket analysis: {str(e)}")

    # Test sales forecasting
    try:
        test_data = {"product_name": "Coffee Maker", "periods": 7}
        response = requests.post(f"{backend_url}/sales-forecast", json=test_data)
        if response.status_code == 200:
            forecast = response.json()
            print(f"✅ Sales forecasting: Generated forecast")
        else:
            print("❌ Sales forecasting: Failed")
    except Exception as e:
        print(f"❌ Sales forecasting: {str(e)}")

    return True


def main():
    print("🚀 SETTING UP RETAILIQ FOR TESTING")
    print("=" * 50)

    # Upload training data
    upload_success = upload_training_data()

    if upload_success:
        # Test API endpoints
        test_api_endpoints()

        print("\n" + "=" * 50)
        print("🎉 SETUP COMPLETE!")
        print("📱 Frontend: http://localhost:5174/")
        print("🔧 Backend: http://localhost:5000/")
        print("\n💡 You can now:")
        print("   1. Visit the frontend to test the application")
        print("   2. Upload additional data via the Data Upload page")
        print("   3. Test market basket analysis and sales forecasting")
        print("   4. Get AI-powered product recommendations")
    else:
        print("\n❌ Setup failed. Please check the backend is running.")


if __name__ == "__main__":
    main()
