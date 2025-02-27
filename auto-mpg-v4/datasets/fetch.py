import pandas as pd

URL = "hf://datasets/scikit-learn/auto-mpg/auto-mpg.csv"
df = pd.read_csv(URL)
df.to_parquet("auto-mpg.parquet", index=False)
