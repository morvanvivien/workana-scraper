"""Minimal example: run the workana-projects-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "keywords": "wordpress",
    "publishedWithinDays": 7,
    "maxItems": 50,
    "onlyNew": False,
    "includeDescriptions": False,
}

run = client.actor("bibian/workana-projects-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    count += 1
    print(f"{item['title']} | {item.get('locationLabel')} | {item.get('budgetLabel')} | {item.get('industry')}")
print(f"{count} results")
