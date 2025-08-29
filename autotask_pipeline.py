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

# 🔹 Start with no filter
body = {
    "filter": []
}

tickets = []
next_url = f"{API_ZONE}/v1.0/Tickets/query"

while next_url:
    print(f"Fetching: {next_url}")
    resp = requests.post(next_url, headers=headers, json=body if next_url.endswith("/query") else None)

    if resp.status_code != 200:
        raise Exception(f"Error {resp.status_code}: {resp.text}")

    data = resp.json()
    items = data.get("items", [])
    tickets.extend(items)

    # pagination
    next_url = data.get("pageDetails", {}).get("nextPageUrl")

# Save to DataFrame
df = pd.DataFrame(tickets)
df.to_csv(CSV_FILE, index=False)
print(f"✅ Saved {len(df)} tickets to {CSV_FILE}")
