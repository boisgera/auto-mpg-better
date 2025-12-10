import marimo

__generated_with = "0.11.31"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import json
    return (json,)


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    import onnx; from onnx import helper, TensorProto
    import onnxruntime as ort
    import pandas as pd
    import seaborn as sns
    return TensorProto, helper, np, onnx, ort, pd, plt, sns


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
    return gpm, lp100


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

    lp100_pred(1000.0)
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
    stats = pred_error.describe()
    stats
    return (stats,)


@app.cell
def _(plt, pred_error, sns):
    sns.histplot(data=pred_error, kde=True)
    plt.grid(True)
    plt.savefig("images/error.png")
    plt.gca()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Artifacts

        We save the results of the learning process in two structures:

          - a result file that contains the model weights and
            expected performance,

          - a model file that can be
            executed by many compatible runtime environments.
        """
    )
    return


@app.cell
def _(intercept, slope, stats):
    results = {
        "model" : {
            "weight": slope,
            "bias": intercept,
        },
        "error" : {
            "mean": stats["mean"],
            "std": stats["std"],
        }
    }
    results
    return (results,)


@app.cell
def _(json, results):
    JSON_PATH = "models/results.json"

    with open(JSON_PATH, mode="wt", encoding="utf-8") as json_file:
        json.dump(results, json_file)
    return JSON_PATH, json_file


@app.cell
def _(TensorProto, helper, intercept, np, onnx, slope):
    ONNX_PATH = "models/lp100.onnx"

    def create_onnx_model(onnx_path=ONNX_PATH):
        slope_array = np.array([[slope]], dtype=np.float64)
        intercept_array = np.array([intercept], dtype=np.float64)

        weight_kg = helper.make_tensor_value_info(
            "weight_kg",
            TensorProto.DOUBLE,
            [None, 1],
        )

        lp100 = helper.make_tensor_value_info(
            "lp100",
            TensorProto.DOUBLE,
            [None, 1],
        )

        slope_initializer = helper.make_tensor(
            name="slope",
            data_type=TensorProto.DOUBLE,
            dims=slope_array.shape,
            vals=slope_array.flatten().tolist(),
        )

        intercept_initializer = helper.make_tensor(
            name="intercept",
            data_type=TensorProto.DOUBLE,
            dims=intercept_array.shape,
            vals=intercept_array.flatten().tolist(),
        )

        matmul_node = helper.make_node(
            "MatMul",
            inputs=["weight_kg", "slope"],
            outputs=["matmul_output"],
        )

        add_node = helper.make_node(
            "Add",
            inputs=["matmul_output", "intercept"],
            outputs=["lp100"],
        )

        graph = helper.make_graph(
            nodes=[matmul_node, add_node],
            name="LP100_Model",
            inputs=[weight_kg],
            outputs=[lp100],
            initializer=[slope_initializer, intercept_initializer],
        )

        model = helper.make_model(graph)
        # Conservative version values to improve runtime compatibility
        model.ir_version = 9
        model.opset_import[0].version = 14
        onnx.checker.check_model(model)
        onnx.save(model, onnx_path)
        print(f"ONNX model saved to {onnx_path}")

        return model


    onnx_model = create_onnx_model()
    return ONNX_PATH, create_onnx_model, onnx_model


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Let's demonstrate how to use this saved ONNX model with the ONNX runtime.

        First we create a callable model instance `onnx_lp100`:
        """
    )
    return


@app.cell
def _(ONNX_PATH, mo, np, onnx_model, ort):
    onnx_model

    class ONNX_LP100:
        def __init__(self):
            self.session = ort.InferenceSession(ONNX_PATH)
        def __call__(self, weight_kg):
            input_shape = np.shape(weight_kg)
            input_is_scalar = np.isscalar(weight_kg)
            weight_kg = np.reshape(weight_kg, (-1, 1))
            lp100 = self.session.run(["lp100"], {"weight_kg": weight_kg})
            lp100 = np.reshape(lp100, input_shape)
            if input_is_scalar:
                lp100 = lp100.item()
            return lp100

    onnx_lp100 = ONNX_LP100()        
    mo.show_code()
    return ONNX_LP100, onnx_lp100


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Then we call this model, either with scalar of vector input data:""")
    return


@app.cell
def _(mo, onnx_lp100):
    mo.show_code(onnx_lp100(weight_kg=1000.0))
    return


@app.cell
def _(dfr, mo, np, onnx_lp100, plt, sns):
    sns.scatterplot(
        x=dfr.weight_kg,
        y=dfr.lp100,
        color="C0",
        alpha=0.25,
        label="data",
    )
    weights_kg = np.arange(500.0, 2500.0 + 0.1, 250.0)
    plt.plot(
        weights_kg, onnx_lp100(weights_kg), "--", color="C0", label="prediction"
    )
    plt.xlabel(
        "weight_kg",
    )
    plt.ylabel("lp100")
    plt.grid(True)
    plt.legend()
    mo.show_code(plt.gcf())
    return (weights_kg,)


if __name__ == "__main__":
    app.run()
