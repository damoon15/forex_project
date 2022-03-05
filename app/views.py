#from app import app
import base64
import io
from flask import Flask, request, redirect
from flask import render_template
from matplotlib import pyplot as plt
from datetime import datetime,timedelta
from func_pool import create_data, get_dates, get_prediction, plot_data, input_dates, create_model, get_peaks, get_seasonal
from utils_forex import data

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')


#@app.route('/', methods=['POST'])
@app.route('/build_plot')
def build_plot():

    img = io.BytesIO()
    train_start_date, train_end_date, test_start_date, test_end_date = input_dates()
    train_data, test_data = create_data(data, train_start_date ,train_end_date, test_start_date, test_end_date)
    model = create_model(train_data)
    predictions, residual = get_prediction(model, test_data)
    ###############plot predictions############################
    fig1, ax1 = plt.subplots(figsize=(10,4))
    ax1.plot(test_data)
    ax1.plot(predictions)
    ax1.legend(('Data', 'Predictions'), fontsize=16)
    ax1.set_title('Japanese Yen/Australian Dollar', fontsize=20)
    ax1.set_ylabel('Close', fontsize=16)
    fig1.savefig(img, format='png')
    img.seek(0)
    ##############################################################
    img1 = io.BytesIO()
    seasonal = get_seasonal(predictions)
    df = get_peaks(seasonal, n=2)
    #############################plot############################
    fig2 , ax2 = plt.subplots()
    ax2.scatter(df.index, df['min'], c='r')
    ax2.scatter(df.index, df['max'], c='g')
    ax2.plot(df.index, df['data'])
    #y = [1,2,3,4,5]
    #x = [0,2,1,3,4]
    #plt.plot(x,y)
    fig2.savefig(img1, format='png')
    img1.seek(0)
    ####################################################################
    plot_url = base64.b64encode(img.getvalue()).decode()
    plot_url1 = base64.b64encode(img1.getvalue()).decode()
    out = "data:image/png;base64,{}".format(plot_url)
    out1 = "data:image/png;base64,{}".format(plot_url1)
    list = [out, out1]

    return render_template('predictions.html', graphs=list)
    #return render_template(graphs=list)


if __name__ == "__main__":
    app.run(debug=True, port=5000)