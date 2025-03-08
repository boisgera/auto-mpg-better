import json

import pandas as pd
import requests

bib_items = json.load(open("../references.json"))
for bib_item in bib_items:
    if bib_item["id"] == "auto_mpg_9":
        csv_url = bib_item["URL"]
        assert csv_url.endswith(".csv")
        break

with open("auto-mpg.csv", "wt", encoding="utf-8") as f:
    f.write(requests.get(csv_url).text)
    
df = pd.read_csv(csv_url)
df.to_parquet("auto-mpg.parquet", index=False)
