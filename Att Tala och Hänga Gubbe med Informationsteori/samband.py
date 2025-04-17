import numpy as np
from sklearn.linear_model import LinearRegression
from data import x_and_y_values



data = x_and_y_values

x_vals = []
y_vals = []

for x, y_list in data.items():
    x_vals.extend([x] * len(y_list))
    y_vals.extend(y_list)



x_vals = np.array(x_vals).reshape(-1, 1)
y_vals = np.array(y_vals)



model = LinearRegression(fit_intercept=False)
model.fit(x_vals, y_vals)



slope = model.coef_[0]
print(f"y = {slope:.2f}x")