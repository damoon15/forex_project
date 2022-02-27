#from app import app
import base64
import io
from flask import Flask, request
from flask import render_template
from matplotlib import pyplot as plt
from datetime import datetime,timedelta
from func_pool import create_data, get_dates, get_prediction, plot_data, input_dates, create_model
from utils_forex import data

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')




@app.route('/plot')
def build_plot():

    img = io.BytesIO()

    train_start_date, train_end_date, test_start_date, test_end_date = input_dates()
    train_data, test_data = create_data(data, train_start_date ,train_end_date, test_start_date, test_end_date)
    model = create_model(train_data)
    predictions, residual = get_prediction(model, test_data)
    plot_data(test_data, predictions)
    plt.figure(figsize=(10,4))
    plt.plot(test_data)
    plt.plot(predictions)
    plt.legend(('Data', 'Predictions'), fontsize=16)
    plt.title('Japanese Yen/Australian Dollar', fontsize=20)
    plt.ylabel('Close', fontsize=16)
    #y = [1,2,3,4,5]
    #x = [0,2,1,3,4]
    #plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)


if __name__ == "__main__":
    app.run(debug=True, port=5000)