
import numpy as np
from sklearn.linear_model import LinearRegression

class BankRegression(LinearRegression):

    def __init__(self):
        super().__init__()

    def fit(self, *args, **kwargs):
        super().fit(*args, **kwargs)
        return self.coef_, self.intercept_

    def get_slope(self):
        return self.coef_

    def get_intercept(self):
        return self.intercept_
