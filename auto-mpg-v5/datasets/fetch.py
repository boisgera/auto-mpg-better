import json

import pandas as pd
import requests

with open("../references.json", encoding="utf-8") as references:
    bibliography = json.load(references)
    for item in bibliography:
        if item["id"] == "auto_mpg_9":
            auto_mpg_9 = item
            break
    else:
        raise ValueError("auto_mpg_9 reference not found")

csv_url = auto_mpg_9["URL"]
assert csv_url.endswith(".csv")

with open("auto-mpg.csv", mode="wt", encoding="utf-8") as csv_file:
    response = requests.get(csv_url)
    response.raise_for_status()
    csv_file.write(response.text)

# Convert CSV to Parquet    
df = pd.read_csv(csv_url)
df.to_parquet("auto-mpg.parquet", index=False)
