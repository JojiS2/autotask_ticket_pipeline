import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
USERNAME = os.getenv("AUTOTASK_USERNAME")
PASSWORD = os.getenv("AUTOTASK_PASSWORD")
TRACKING_ID = os.getenv("AUTOTASK_TRACKING_IDENTIFIER")
API_ZONE = os.getenv("AUTOTASK_API_ZONE")

CSV_FILE = "tickets.csv"

headers = {
    "ApiIntegrationCode": TRACKING_ID,
    "UserName": USERNAME,
    "Secret": PASSWORD,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Try different body formats
bodies = [
    {
        "filter": [
            {"op": "gte", "field": "createDate", "value": "2025-05-13T00:00:00Z"}
        ]
    },
    {
        "queryModel": {
            "filter": [
                {"op": "gte", "field": "createDate", "value": "2025-05-13T00:00:00Z"}
            ]
        }
    },
    {
        "queryModel": {
            "filters": [
                {"op": "gte", "field": "createDate", "value": "2025-05-13T00:00:00Z"}
            ]
        }
    }
]

url = f"{API_ZONE}/v1.0/Tickets/query"
tickets = []

for body in bodies:
    print(f"🔎 Trying body format: {body}")
    resp = requests.post(url, headers=headers, json=body)
    print("Status:", resp.status_code)

    if resp.status_code == 200:
        data = resp.json()
        tickets = data.get("items", [])
        print(f"✅ Success with this format! Got {len(tickets)} tickets.")
        break
    else:
        print("❌ Failed with:", resp.text)

if not tickets:
    raise Exception("All body formats failed. Check API docs for your zone.")

# Save to CSV
df = pd.DataFrame(tickets)
if not df.empty:
    df.to_csv(CSV_FILE, index=False)
    print(f"Saved {len(df)} tickets to {CSV_FILE}")
else:
    print("⚠️ No tickets returned.")
