# ft_linear_regression

**ft_linear_regression** is a 42 school project introducing the fundamentals of **machine learning** through the implementation of a simple **linear regression** algorithm trained with **gradient descent**.

## Overview

The goal of this project is to predict the price of a car based on its mileage using a linear hypothesis.
The model is trained from a dataset and can then be reused to estimate prices for new inputs.

The project is split into:
- a **training program** (`train.py`) that learns the model parameters
- a **prediction program** (`predict.py`) that uses the trained model
- a **precision program** (`precision.py`) that evaluates the trained model

The full project, including **all bonuses**, is implemented.

## Features

* Linear regression with **one feature** (mileage)
* Training using **gradient descent**
* Persistent model parameters (`theta0`, `theta1`) saved in a `weights` file
* Separate programs for training, prediction and precision
* Dataset read from `data.csv`, with or without a header line
* Data visualization (bonus)
* Model precision evaluation (bonus)

## Model

The hypothesis used to estimate the price is:
```
estimatePrice(mileage) = θ0 + (θ1 × mileage)
```
Model parameters are initialized to:
```
θ0 = 0
θ1 = 0
```

They are updated during training using gradient descent. Without a `weights` file, `predict.py` falls back to these initial values (so every estimate is 0).

## Gradient Descent

Gradient Descent is an optimization algorithm used to minimize a cost function.
In this project, it is used to find the best parameters (θ₀ and θ₁) of a linear regression model by iteratively updating them in the opposite direction of the gradient.

At each iteration, the algorithm slightly adjusts the parameters to reduce the prediction error.
Over time, this process makes the regression line converge toward the best possible fit for the data.

θ₀ and θ₁ are updated **simultaneously**: both gradients are computed from the same predictions, made with the previous values of the parameters.

### Normalization

Mileages are in the order of 10⁵ while the prices are in the order of 10³–10⁴. With such different scales, gradient descent would diverge or converge very slowly.
The training therefore runs on normalized data (mileages and prices divided by their maximum), then the parameters are converted back to the real scale before being saved:
```
θ0_real = θ0 × max(price)
θ1_real = θ1 × max(price) / max(mileage)
```
The formulas of the subject are unchanged: they are simply applied to scaled data.

## Mean Squared Error (MSE)

Mean Squared Error (MSE) is a metric used to measure how well a model predicts the target values.
It computes the average of the squared differences between the predicted values and the actual values.

In this project, the MSE is used to monitor the convergence of the Gradient Descent algorithm.
A decreasing MSE indicates that the model is learning and improving its predictions.
The MSE displayed during training is computed on the normalized data.

## Usage
### Training the model
```bash
python3 train.py
```

This program:
- reads the dataset
- trains the model using gradient descent
- saves theta0 and theta1 in the `weights` file for later use
- prints the final parameters and displays the plots

### Predicting a price
```bash
python3 predict.py
```

The program prompts for a mileage and outputs the estimated car price using the trained model.

### Computing the precision
```bash
python3 precision.py
```

The program loads the trained parameters, predicts the price of every car of the dataset and prints the coefficient of determination / correlation (R²) as a percentage.
It requires `train.py` to have been run first.

## Bonus

- **Dataset plot**: scatter plot of the mileages and prices to visualize the distribution
- **Regression line**: line resulting from the linear regression, drawn on the same graph as the data
- **Training history**: the values of theta0 and theta1 are recorded at every iteration. They are used to replay the training with an interactive slider: moving it shows how the regression line evolves from the initial state (a flat line at 0) to the final fit
- **MSE loss curve**: evolution of the error over the iterations, showing the convergence of the algorithm
- **Precision calculation**: `precision.py` evaluates the model with the coefficient of determination / correlation R² (1 means a perfect fit, 0 means no better than predicting the mean price)
