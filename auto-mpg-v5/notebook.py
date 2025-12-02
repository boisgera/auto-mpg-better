import marimo

__generated_with = "0.11.31"
app = marimo.App()


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
def _(intercept, np, slope):
    def lp100_pred(weight_kg):
        return intercept + slope * weight_kg

    lp100_pred(np.float32(1000.0))
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


@app.cell
def _(TensorProto, helper, intercept, np, onnx, slope):
    MODEL_PATH = "models/lp100.onnx"

    def create_onnx_model(model_path=MODEL_PATH):
        slope_array = np.array([[slope]], dtype=np.float32)
        intercept_array = np.array([intercept], dtype=np.float32)

        weight_kg = helper.make_tensor_value_info(
            "weight_kg",
            TensorProto.FLOAT,
            [None, 1],
        )

        lp100 = helper.make_tensor_value_info(
            "lp100",
            TensorProto.FLOAT,
            [None, 1],
        )

        slope_initializer = helper.make_tensor(
            name="slope",
            data_type=TensorProto.FLOAT,
            dims=slope_array.shape,
            vals=slope_array.flatten().tolist(),
        )

        intercept_initializer = helper.make_tensor(
            name="intercept",
            data_type=TensorProto.FLOAT,
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
        model.ir_version = 9
        model.opset_import[0].version = 14
        onnx.checker.check_model(model)
        onnx.save(model, model_path)
        print(f"Model saved to {model_path}")

        return model


    create_onnx_model()
    return MODEL_PATH, create_onnx_model


@app.cell
def _(MODEL_PATH, np, ort):

    def run_siso_model(session, input_value):
        """
        Run a SISO ONNX model with a single input value
    
        Args:
            onnx_path: Path to the ONNX file
            input_value: Single float input value
            use_gpu: Whether to use GPU (CUDA) if available
    
        Returns:
            Model output as a float
        """
        # Create session options

        # Get input and output names
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
    
        # Prepare input data
        # Convert scalar to 2D array: [batch_size, input_dimension]
        # For SISO: shape should be [1, 1] for single sample
        input_data = np.array([[input_value]], dtype=np.float32)
    
        # Run inference
        outputs = session.run([output_name], {input_name: input_data})
    
        # Extract output (assuming single output)
        output_value = outputs[0][0][0]  # Get scalar from [1, 1] array
    
        return output_value

    options = ort.SessionOptions()
    # Load the ONNX model
    session = ort.InferenceSession(MODEL_PATH, options)

    # Single input value
    input_value = 1000

    # Run inference
    try:
        output = run_siso_model(session, input_value)
        print(f"Input: {input_value}, Output: {output}")
    except Exception as e:
        print(f"Error: {e}")
    return input_value, options, output, run_siso_model, session


if __name__ == "__main__":
    app.run()
