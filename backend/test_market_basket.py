import requests
import json

# Test market basket analysis response structure
response = requests.post(
    "http://localhost:5000/market-basket-analysis",
    headers={"Content-Type": "application/json"},
    json={"min_support": 0.01, "min_confidence": 0.2},
)

if response.status_code == 200:
    data = response.json()
    rules = data["data"]["analysis"]["association_rules"]
    print("Association Rules structure:")
    if rules:
        print(f"First rule: {json.dumps(rules[0], indent=2)}")
        print(f"Number of rules: {len(rules)}")
    else:
        print("No rules found")
else:
    print(f"Error: {response.status_code} - {response.text}")
