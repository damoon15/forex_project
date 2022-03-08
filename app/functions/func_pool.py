from utils_forex import data, toDate
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
import pickle
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import STL
from flask import request
from scipy.signal import argrelextrema
import numpy as np


def create_data(data, train_start_date, train_end_date, test_start_date, test_end_date):
    close_data = data['Close']
    close_data = close_data.interpolate()
    #test_data = close_data[test_start_date:test_end_date]
    #train_data = close_data[:test_start_date - timedelta(days=1)]
    train_data = close_data[train_start_date: train_end_date]
    test_data = close_data[test_start_date: test_end_date]

    #train_end = close_data.index.max() - timedelta(days=10)
    #test_end = close_data.index.max()
    #train_data = close_data[:train_end]
    #test_data = close_data[train_end + timedelta(days=1):test_end]
    return train_data, test_data

def create_model(train_data):
    model = SARIMAX(train_data, order=(0,1,0), seasonal_order = (1, 1, 1, 7))
    model_output = model.fit(maxiter=500, method='nm')
    with open('./model_sarima.pkl', 'wb') as file:
        pickle.dump(model_output, file)
    return model_output

def get_dates(test_data):
    start_date = test_data.index[0]
    end_date = test_data.index[-1]
    return start_date, end_date

def get_prediction_res(model, test_data):
    start_date = test_data.index[0]
    end_date = test_data.index[-1]
    predictions = model.predict(start=start_date, end=end_date)
    residuals = test_data - predictions
    error_percent = np.divide(residuals,test_data)*100
    return predictions, residuals, error_percent

def plot_data(test_data, predictions):
    plt.figure(figsize=(10,4))
    plt.plot(test_data)
    plt.plot(predictions)
    plt.legend(('Data', 'Predictions'), fontsize=16)
    plt.title('Japanese Yen/Australian Dollar', fontsize=20)
    plt.ylabel('Close', fontsize=16)


def input_dates():
    dates_train = request.args.getlist('dates_entry_train', type=toDate)
    train_start_date = dates_train[0]
    train_end_date = dates_train[1]
    dates_test = request.args.getlist('dates_entry_test', type=toDate)
    test_start_date = dates_test[0]
    test_end_date = dates_test[1]
    return train_start_date, train_end_date, test_start_date, test_end_date
def get_seasonal(data):
    stl = STL(data)
    result = stl.fit()
    seasonal, trend, resid = result.seasonal, result.trend, result.resid
    return seasonal
def get_peaks(seasonal, n):
    df = seasonal.to_frame(name='data')
    df['min'] = df.iloc[argrelextrema(df.data.values, np.less_equal,order=n)[0]]['data']
    df['max'] = df.iloc[argrelextrema(df.data.values, np.greater_equal,order=n)[0]]['data']
    return df
def get_prediction(model, start_date, end_date):
    predictions = model.predict(start=start_date, end=end_date)
    return predictions

if __name__=='__main__':
    #train_data, test_data = create_data(data)
    #start_date, end_date = get_dates(test_data)
    #a, b = get_prediction(model, test_data, start_date, end_date)
    #plot_data(test_data, a)
    #future_predict = get_prediction(model, date.today(), date.today() + timedelta(days=3))
    seasonal_prediction = get_prediction(model, data.index[190], date.today()+timedelta(days=3))
    future_predict = get_prediction(model, date.today() - timedelta(days=9), date.today() + timedelta(days=3))