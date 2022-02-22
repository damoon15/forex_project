from utils_forex import model, data
from datetime import datetime,timedelta
import matplotlib.pyplot as plt


#%%
def create_data(data):
    close_data = data['Close']
    close_data = close_data.interpolate()
    train_end = close_data.index.max() - timedelta(days=10)
    test_end = close_data.index.max()
    train_data = close_data[:train_end]
    test_data = close_data[train_end + timedelta(days=1):test_end]
    return train_data, test_data

def get_dates(test_data):
    start_date = test_data.index[0]
    end_date = test_data.index[-1]
    return start_date, end_date

def get_prediction(model, test_data, start_date, end_date):
    predictions = model.predict(start=start_date, end=end_date)
    residuals = test_data - predictions
    return predictions, residuals

def plot_data(test_data, predictions):
    plt.figure(figsize=(10,4))
    plt.plot(test_data)
    plt.plot(predictions)
    plt.legend(('Data', 'Predictions'), fontsize=16)
    plt.title('Japanese Yen/Australian Dollar', fontsize=20)
    plt.ylabel('Close', fontsize=16)


if __name__=='__main__':
    train_data, test_data = create_data(data)
    start_date, end_date = get_dates(test_data)
    a, b = get_prediction(model, test_data, start_date, end_date)
    plot_data(test_data, a)