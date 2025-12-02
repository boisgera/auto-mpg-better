import marimo

__generated_with = "0.18.0"
app = marimo.App()


@app.cell
def _():
    import json
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns
    return np, pd, plt, sns


@app.cell
def _(pd):
    df = pd.read_parquet("datasets/auto-mpg.parquet")
    df
    return (df,)


@app.cell
def _(df, sns):
    sns.pairplot(df, hue="origin")
    return


@app.cell
def _(df, plt, sns):
    sns.scatterplot(data=df, x="weight", y="mpg", hue="origin")
    plt.grid(True)
    plt.gca()
    return


@app.cell
def _(df):
    gpm = (1.0 / df.mpg)
    lp100 = gpm * 3.78541 / 1.60934 * 100
    lp100 = lp100.rename("lp100")
    return (lp100,)


@app.cell
def _(df):
    weight_kg = df.weight * 0.453592
    weight_kg = weight_kg.rename("weight_kg")
    return (weight_kg,)


@app.cell
def _(lp100, pd, weight_kg):
    dfr = pd.DataFrame({lp100.name: lp100, weight_kg.name: weight_kg})
    dfr
    return (dfr,)


@app.cell
def _(dfr, sns):
    sns.pairplot(dfr)
    return


@app.cell
def _(dfr, np):
    coeffs, _, _, _ = np.linalg.lstsq(
        a=np.stack([dfr.weight_kg, np.ones_like(dfr.weight_kg)], axis=1),
        b=dfr.lp100,
    )
    coeffs
    return (coeffs,)


@app.cell
def _(coeffs):
    slope, intercept = coeffs
    return intercept, slope


@app.cell
def _(intercept, slope):
    def lp100_pred(weight_kg):
        return intercept + slope * weight_kg
    return (lp100_pred,)


@app.cell
def _(dfr, lp100_pred, plt, sns):
    sns.scatterplot(x=dfr.weight_kg, y=dfr.lp100, color="C0", alpha=0.25)
    plt.plot(dfr.weight_kg, lp100_pred(dfr.weight_kg), color="C0")
    plt.grid(True)
    plt.savefig("images/prediction.png")
    plt.gca()
    return


@app.cell
def _(dfr, lp100_pred):
    pred_error = lp100_pred(dfr.weight_kg) - dfr.lp100
    pred_error = pred_error.rename("pred_error")
    pred_error
    return (pred_error,)


@app.cell
def _(pred_error):
    pred_error.describe()
    return


@app.cell
def _(plt, pred_error, sns):
    sns.histplot(data=pred_error, kde=True)
    plt.grid(True)
    plt.savefig("images/error.png")
    plt.gca()
    return


if __name__ == "__main__":
    app.run()
