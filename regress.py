
import numpy as np
from sklearn.linear_model import LinearRegression

class BankRegression(LinearRegression):

    def __init__(self):
        super().__init__()
