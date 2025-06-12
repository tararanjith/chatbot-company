import json
import os

def load_website_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "website.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)
