import json
import math

from jinja2 import Template

def float_to_latex(number):
    if math.isnan(number):
        return r'\text{NaN}'
    if math.isinf(number):
        return r'\infty' if number > 0 else r'-\infty'
    if number == 0 or number == 0.0:
        return '0'
    
    python_repr = repr(number)
    if 'e' in python_repr.lower():
        # Parse the scientific notation
        parts = python_repr.lower().split('e')
        mantissa = parts[0]
        exponent = int(parts[1])
        return rf'{mantissa} \times 10^{{{exponent}}}'
    else:
        return python_repr


with open("../models/results.json", mode="rt", encoding="utf-8") as results_file: 
    results = json.load(results_file)


with open("../article.md.j2", mode="rt", encoding="utf-8") as template_file:
    template = Template(template_file.read())

weight = results["model"]["weight"]
bias = results["model"]["bias"]
mean = results["error"]["mean"]
std = results["error"]["std"]

MAX_MEAN = 1e-3
MAX_STD = 2.0

assert abs(mean) <= MAX_MEAN
assert std <= MAX_STD

filled = template.render(
    slope=float_to_latex(weight), 
    intercept=float_to_latex(bias), 
    mean=float_to_latex(mean), 
    std=float_to_latex(std),
    max_mean = float_to_latex(MAX_MEAN),
    max_std = float_to_latex(MAX_STD),
)

with open("../article.md", mode="wt", encoding="utf-8") as article:
    article.write(filled)