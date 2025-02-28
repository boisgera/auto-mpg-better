import json
import os.path

dir = os.path.dirname(__file__)

with open(os.path.join(dir, "coeffs.json"), "r", encoding="utf-8") as file:
    coeffs = json.load(file)

slope = coeffs["slope"]
intercept = coeffs["intercept"]

def lp100_pred(weight_kg):
    return slope * weight_kg + intercept
