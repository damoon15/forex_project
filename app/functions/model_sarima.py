# Raw Package
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#Data Source
import yfinance as yf
#Data viz library
import plotly.graph_objs as go
from statsmodels.tsa.stattools import acf, pacf
from datetime import datetime,timedelta
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import STL
from app.functions.utils_forex import data
from func_pool import create_data
import pickle

#%%
train_data, test_data = create_data(data)
model = SARIMAX(train_data, order=(0,1,0), seasonal_order = (1, 1, 1, 7))
model_output = model.fit(maxiter=500, method='nm')
with open('./model_sarima.pkl', 'wb') as file:
    pickle.dump(model_output, file)

#if __name__ == '__main__':
 #   print('salam')

#%%
