import marimo

__generated_with = "0.11.31"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Managing the AUTO-MPG Dataset

        [Sébastien Boisgérault], Mines Paris - PSL University

        [Sébastien Boisgérault]: mailto:Sebastien.Boisgerault@minesparis.psl.eu
        """
    )
    return


@app.cell
def _():
    # Python Standard Library
    import csv
    import hashlib
    import json
    import pathlib
    return csv, hashlib, json, pathlib


@app.cell
def _():
    # Third-Party Libraries
    import matplotlib.pyplot as plt
    import pandas as pd
    import requests
    import seaborn as sns; sns.set_theme()
    return pd, plt, requests, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Fetch the original dataset""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        🏷️ Auto MPG Dataset (🇺🇸 MPG stands for means "Miles Per Gallon")

        🏛️ UCI Machine Learning Repository

        🔗 DOI: [10.24432/C5859H](https://doi.org/10.24432/C5859H)
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Our CSL-JSON bibliography and its `auto_mpg_9` bibliography item:""")
    return


@app.cell(hide_code=True)
def _(json):
    with open("../bibliography/references.json", encoding="utf-8") as bibliography_file:
        bibliography = json.load(bibliography_file)
    bibliography
    return bibliography, bibliography_file


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
    return DATA_URL, MD5_SUM, auto_mpg_9, item


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
    mo.md(r"""Let's download this file in the current directory and verify the checksum.""")
    return


@app.cell(hide_code=True)
def _(DATA_URL, pathlib, requests):
    r = requests.get(DATA_URL)
    raw_data = r.content
    assert type(raw_data) == bytes
    with open("auto-mpg.csv", mode="bw") as _file:
        _file.write(raw_data)
    pathlib.Path("auto-mpg.csv")
    return r, raw_data


@app.cell(hide_code=True)
def _(MD5_SUM, hashlib):
    with open("auto-mpg.csv", "rb") as _file:
        checksum = hashlib.md5(_file.read()).hexdigest()
    print(f"Checksum: {'✅' if checksum == MD5_SUM else '❌'}")
    return (checksum,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We load the file as a Pandas dataframe:""")
    return


@app.cell
def _(pd):
    df = pd.read_csv("auto-mpg.csv")
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## NA Values

        There are a few not-available values in the data. We remove the corresponding 4 rows.
        """
    )
    return


@app.cell
def _(df, mo):
    mo.show_code(df.isna().any())
    return


@app.cell
def _(df):
    df_1 = df.dropna().reset_index(drop=True)
    df_1
    return (df_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Brands and models

        The brand (company) name and model name are mixed into the `car_name` field. We split it into proper `brand` and `model` fields. There are also quite a few inconsistencies and typos in the automobile brands that we try to fix issues.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r""" """)
    return


@app.cell(hide_code=True)
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

    list(df_2["brand"].unique())
    return brands, car_names, df_2, models, tweak_brand


@app.cell
def _(df_2):
    df_2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Origin

        The `origin` field is a number encoding the origin of the car.
        """
    )
    return


@app.cell
def _(df_2, mo):
    mo.show_code(df_2["origin"].unique())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""A study of the data shows that `1` stands for USA, `2` for Europe and `3` for Asia.""")
    return


@app.cell
def _(df_2):
    df_2[["origin", "brand"]].sort_values(by="origin", ignore_index=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We replace the number with the appropriate name.""")
    return


@app.cell
def _(df_2):
    df_3 = df_2.copy()
    def convert_origin(number):
        return {1: "USA", 2: "Europe", 3: "Asia"}.get(number)
    df_3["origin"] = df_3["origin"].apply(convert_origin)
    return convert_origin, df_3


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Data types

        If we look at the current data types, we see that the weight is encoded as an integer when similar values are encoded as floating-point numbers. Also, the origin is now a string (`object`) when it's actually some categorical data (a label between a fixed number of options).
        """
    )
    return


@app.cell
def _(df_3):
    df_3.dtypes
    return


@app.cell
def _(df_3):
    # ⚠️ These changes would be lost if df_4 was exported as csv ... but not parquet! 🥳
    df_4 = df_3.copy()
    df_4["origin"] = df_3["origin"].astype("category")
    df_4["weight"] = df_4["weight"].astype(float)
    df_4
    return (df_4,)


@app.cell
def _(mo):
    mo.md(r"""We fix both issues.""")
    return


@app.cell
def _(df_4):
    df_4.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Cleaned-up dataset""")
    return


@app.cell
def _(df_4):
    df_4
    return


@app.cell
def _(df_4, sns):
    sns.pairplot(df_4[["model_year", "weight", "origin", "mpg"]], hue='origin')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        We could save the resulting dataset as a csv file, but we would lose some information, since this format does not store the information about data types. Instead, we use the [Apache Parquet] format, which fixes this problem and has other advantages.

        [Apache Parquet]: https://en.wikipedia.org/wiki/Apache_Parquet
        """
    )
    return


@app.cell
def _(df_4, mo):
    mo.show_code(df_4.to_parquet("auto-mpg.parquet"))
    return


if __name__ == "__main__":
    app.run()
