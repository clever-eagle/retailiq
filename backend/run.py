#!/usr/bin/env python3
"""
Retail Analytics Backend Server
Run this script to start the Flask development server
"""

import os
import sys
from app import app

if __name__ == "__main__":
    # Set environment variables
    os.environ.setdefault("FLASK_ENV", "development")

    print("=" * 50)
    print("🚀 Starting Retail Analytics Backend Server")
    print("=" * 50)
    print(f"📊 Server running on: http://localhost:5000")
    print(f"🌐 Frontend should connect to: http://localhost:5000")
    print("=" * 50)
    print("\nAvailable API Endpoints:")
    print("  GET  /health                    - Health check")
    print("  POST /upload-data               - Upload CSV data")
    print("  POST /market-basket-analysis    - Perform market basket analysis")
    print("  POST /get-recommendations       - Get product recommendations")
    print("  POST /sales-forecast            - Generate sales forecast")
    print("  GET  /sales-trends              - Get sales trends")
    print("  GET  /data-summary              - Get data summary")
    print("  POST /frequent-itemsets         - Get frequent itemsets")
    print("=" * 50)
    print("📝 To stop the server, press Ctrl+C")
    print("=" * 50)

    try:
        # Run the Flask app
        app.run(host="0.0.0.0", port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)
