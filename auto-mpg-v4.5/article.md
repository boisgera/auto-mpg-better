---
title: Prediction of Car Fuel Consumption
author: S. Boisgérault
#[[[cog
# import cog
# from datetime import datetime
# today = datetime.today()
# latex_date = today.strftime("%B %d, %Y")
# print(f"date: {latex_date}")
#]]]
date: March 06, 2025
#[[[end]]]
abstract: |
  We produce a model that predicts a vehicle fuel consumption from its weight, 
  with a estimated standard deviation smaller than 2 liters per 100 km. 
  The model is based on the Auto-MPG dataset.
---

# Introduction
**TODO**

# Model

Our model is:
$$
\mbox{fuel consumption} =  0.00899249 \times \mbox{vehicle weight} -0.90305387
$$
where the fuel consumption is measured in liters per 100 km and the vehicle 
weight in kg.

![Fuel consumption vs weight in the auto-mpg data sets (semi-transparent dots) 
and the corresponding prediction model (line).](images/prediction.png)



# Error Distribution

Our model is practically unbiased 
$$
|\mbox{mean}| \leq 10^{-14}
$$
and its standard deviation is
$$
\mbox{std} \approx 1.815 < 2.0.
$$

![The consumption prediction error distribution.](images/error.png)

# Dataset

Auto-mpg comes from @auto_mpg_9.

# References
