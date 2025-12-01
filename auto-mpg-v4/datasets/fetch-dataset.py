import marimo

__generated_with = "0.18.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Managing the AUTO-MPG Dataset

    [Sébastien Boisgérault], Mines Paris - PSL University

    [Sébastien Boisgérault]: mailto:Sebastien.Boisgerault@minesparis.psl.eu
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    /// tip | Learning Objectives
    - [ ] Fetch the data set (use API and CSV to learn both ways),
    - [ ] Explore the metadata, interpret the info,
    - [ ] Make a dataframe from the data,
    - [ ] Make a seaborn pairplot with the suitable hue,
    - [ ] Clean-up: manage NaNs, fix errors, fix data types, get the brands, etc.
    - [ ] Save your result in a suitable format.
    """)
    return


@app.cell
def _():
    # Python Standard Library
    import csv
    import hashlib
    import json
    import pathlib
    return hashlib, json, pathlib


@app.cell
def _():
    # Third-Party Libraries
    import matplotlib.pyplot as plt
    import pandas as pd
    import requests
    import seaborn as sns; sns.set_theme()
    return pd, requests, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Fetch the Dataset
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    🏷️ Auto MPG Dataset (🇺🇸 MPG stands for means "Miles Per Gallon")

    🏛️ UCI Machine Learning Repository

    🔗 DOI: [10.24432/C5859H](https://doi.org/10.24432/C5859H)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Our CSL-JSON bibliography and its `auto_mpg_9` bibliography item:
    """)
    return


@app.cell(hide_code=True)
def _(json):
    with open("../references.json", encoding="utf-8") as bibliography_file:
        bibliography = json.load(bibliography_file)
    bibliography
    return (bibliography,)


@app.cell(hide_code=True)
def _(bibliography):
    for item in bibliography:
        if item["id"] == "auto_mpg_9":
            auto_mpg_9 = item
            break
    else:
        raise ValueError("auto_mpg_9 reference not found")

    DATA_URL = auto_mpg_9["URL"]
    assert auto_mpg_9["custom"]["checksum"]["type"] == "md5"
    MD5_SUM = auto_mpg_9["custom"]["checksum"]["value"]
    assert DATA_URL.endswith(".csv")
    return DATA_URL, MD5_SUM


@app.cell(hide_code=True)
def _(DATA_URL, MD5_SUM, mo):
    mo.md(rf"""
    We can get from this 

    - the URL of the dataset: {DATA_URL}

    - the MD5 checksum of the data it refers to: `{MD5_SUM}`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's download this file in the current directory and verify the checksum.
    """)
    return


@app.cell(hide_code=True)
def _(DATA_URL, pathlib, requests):
    r = requests.get(DATA_URL)
    raw_data = r.content
    assert type(raw_data) == bytes
    with open("auto-mpg.csv", mode="bw") as _file:
        _file.write(raw_data)
    pathlib.Path("auto-mpg.csv")
    return


@app.cell(hide_code=True)
def _(MD5_SUM, hashlib, mo):
    with open("auto-mpg.csv", "rb") as _file:
        checksum = hashlib.md5(_file.read()).hexdigest()
    mo.md(f"Checksum: {'✅' if checksum == MD5_SUM else '❌'}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We load the file as a Pandas dataframe:
    """)
    return


@app.cell
def _(pd):
    df = pd.read_csv("tmp/auto_mpg.csv")
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Cleanup
    """)
    return


@app.cell
def _(df):
    df.isna().any()
    return


@app.cell
def _(df):
    df_1 = df.dropna().reset_index(drop=True)
    df_1
    return (df_1,)


@app.cell
def _(df_1):
    df_2 = df_1.copy()
    car_names = df_1["car_name"]
    brands = [car_name.split(",")[0].strip().capitalize() for car_name in car_names]
    models = [" ".join(car_name.split(",")[1:]).capitalize() for car_name in car_names]
    del df_2["car_name"]
    df_2.insert(0, "brand", brands)
    df_2.insert(1, "model", models)
    df_2 = df_2.sort_values(by="brand", ignore_index=True)
    def tweak_brand(name):
        if len(name) <= 3: # Acronyms: Amc, Bmw, etc.
            name = name.upper()
        fixes = {
            "AMC": "American Motors",
            "HI": "International Harvester",
            "Chevroelt": "Chevrolet",
            "Chevy": "Chevrolet",
            "Toyouta": "Toyota",
            "Maxda": "Mazda",
            "Mercedes-benz": "Mercedes-Benz",
            "Mercedes": "Mercedes-Benz",
            "Vokswagen": "Volkswagen",
            "VW": "Volkswagen",

        }
        name = fixes.get(name) or name
        return name
    df_2["brand"] = df_2["brand"].apply(tweak_brand)
    df_2 = df_2.sort_values(by="brand", ignore_index=True)

    df_2["brand"].unique()
    return (df_2,)


@app.cell
def _(df_2):
    df_2
    return


@app.cell
def _(df_2):
    df_2["origin"].unique()
    return


@app.cell
def _(df_2):
    df_2[["origin", "brand"]].sort_values(by="origin", ignore_index=True)
    return


@app.cell
def _(df_2):
    df_3 = df_2.copy()
    def convert_origin(number):
        return {1: "USA", 2: "Europe", 3: "Asia"}.get(number)
    df_3["origin"] = df_3["origin"].apply(convert_origin)
    df_3
    return (df_3,)


@app.cell
def _(df_3, sns):
    sns.pairplot(df_3[["model_year", "weight", "origin", "mpg"]], hue='origin')
    return


@app.cell
def _(df_3):
    df_3
    return


@app.cell
def _(df_3):
    # ⚠️ These changes will be lost if df_4 is exported as csv ... but not parquet! 🥳
    df_4 = df_3.copy()
    df_4["origin"] = df_3["origin"].astype("category")
    df_4["weight"] = df_4["weight"].astype(float)
    df_4
    return (df_4,)


@app.cell
def _():
    #df_4.to_csv("data/auto_mpg.csv", index=False)
    return


@app.cell(hide_code=True)
def _():
    #pd.read_csv("data/auto_mpg.csv")
    return


@app.cell
def _(df_4):
    df_4.to_parquet("auto-mpg.parquet")
    return


@app.cell
def _(pd):
    pd.read_parquet("auto-mpg.parquet")
    return


if __name__ == "__main__":
    app.run()
