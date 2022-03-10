#from app import app
import base64
import io
from flask import Flask, request, redirect
from flask import render_template
from matplotlib import pyplot as plt
from datetime import datetime,timedelta, date

import matplotlib
from app.functions.func_pool import create_data, get_dates, get_prediction_res, get_prediction, plot_data, input_dates, create_model, get_peaks, get_seasonal
from app.functions.utils_forex import data
import matplotlib.dates as mdates

app = Flask(__name__)
@app.route('/')
def home():
    list = ["", "", "", "","",""]
    return render_template('predictions.html', graphs= list)


#@app.route('/', methods=['POST'])
@app.route('/build_plot')
def build_plot():
    matplotlib.use("agg")

    img = io.BytesIO()
    train_start_date, train_end_date, test_start_date, test_end_date = input_dates()
    train_data, test_data = create_data(data, train_start_date ,train_end_date, test_start_date, test_end_date)
    model = create_model(train_data)
    predictions, residual, error_percent = get_prediction_res(model, test_data)

    #%%model_performance:
    fig1, ax1 = plt.subplots(figsize=(10,4))
    x_t = test_data.index
    x_t_str = [str(i) for i in x_t]
    ax1.plot(x_t, test_data, linestyle='dashed', marker='s')
    ax1.plot(x_t, predictions, linestyle='dashed', marker='s')
    label0 = "error = {:.2f}%".format(abs(error_percent[0]))
    ax1.annotate(label0, xy=(mdates.date2num(x_t[0])-0.15, predictions[0]-0.00002), xycoords='data')
    for i in range(1, len(x_t)):
        label = "error = {:.2f}%".format(abs(error_percent[i]))
        ax1.annotate(label, xy=(mdates.date2num(x_t[i])-0.27, predictions[i]-0.00002), xycoords='data')
    ax1.set_xticks(x_t)
    ax1.set_xticklabels(x_t_str)
    ax1.legend(('Data', 'Predictions'), fontsize=16)
    ax1.set_title('Japanese Yen/Australian Dollar', fontsize=20)
    ax1.set_ylabel('Close Rate', fontsize=16)
    fig1.savefig(img, format='png')
    img.seek(0)
    #%% peaks:
    img1 = io.BytesIO()
    seasonal_prediction = get_prediction(model, train_data.index[0], date.today()+timedelta(days=3))
    seasonal = get_seasonal(seasonal_prediction)
    df = get_peaks(seasonal, n=3)
    df_plot = df.loc[date.today()-timedelta(days=15):]
    fig2 , ax2 = plt.subplots()
    ax2.scatter(df_plot.index, df_plot['min'], c='r')
    ax2.scatter(df_plot.index, df_plot['max'], c='g')
    ax2.plot(df_plot.index, df_plot['data'])
    #ax2.set_xticks(rotation=90)
    fig2.autofmt_xdate(rotation=45)
    #ax2.plot([str(i) for i in df_plot.index], df_plot['data'], linestyle='dashed', marker='s')
    ax2.set_title('Seasonal peaks of the predicted data', fontsize=20)
    ax2.set_ylabel('Close Rate', fontsize=16)
    ax2.set_xlabel('Date', fontsize=16)
    fig2.savefig(img1, format='png')
    img1.seek(0)
    #%% future prediction
    img2 = io.BytesIO()
    fig3, ax3 = plt.subplots(figsize=(12,6))
    #ax3.set_xlim(-.4,.4)
    #ax3.set_ylim(-.4,.4)
    future_predict = get_prediction(model, date.today(), date.today() + timedelta(days=3))
    x = future_predict.index
    x_dates = mdates.date2num([x])
    x_str = [str(i) for i in x]
    #ax3.plot(x_str, future_predict, linestyle='dashed', marker='s')
    ax3.plot(x, future_predict, linestyle='dashed', marker='s')
    ax3.set_xticks(x)
    ax3.set_xticklabels(x_str)
    #for i in range(len(x)):
    label0 = "close_rate = {:.6f}".format(future_predict[0])
    ax3.annotate(label0, xy=(mdates.date2num(x[0]), future_predict[0]+0.000003), xycoords='data')
    label1 = "close_rate = {:.6f}".format(future_predict[1])
    ax3.annotate(label1, xy=(mdates.date2num(x[1])+0.05, future_predict[1]), xycoords='data')
    label2 = "close_rate = {:.6f}".format(future_predict[2])
    ax3.annotate(label2, xy=(mdates.date2num(x[2])+0.05, future_predict[2]), xycoords='data')
    label3 = "close_rate = {:.6f}".format(future_predict[3])
    ax3.annotate(label3, xy=(mdates.date2num(x[3])-0.6, future_predict[3]), xycoords='data')


    #ax3.plot(future_predict)
    #for i, j in zip(x_dates, future_predict):

    #    label = "{:.2f}".format(j)
    #ax3.text(x_dates[0], future_predict[0], "salam", color='red')
    #ax3.annotate('Test', xy=(mdates.date2num(x[1]), future_predict[1]), xycoords='data')
    #fig3.autofmt_xdate()
    #ax3.text(, future_predict[i], "close = {}".format(future_predict[i]))
    #ax3.plot(future_predict)
    ax3.set_title('Future prediction for Japanese Yen/Australian Dollar', fontsize=20)
    ax3.set_ylabel('Close Rate', fontsize=16)
    fig3.savefig(img2, format='png')
    img2.seek(0)
    #%% prepare for html
    plot_url = base64.b64encode(img.getvalue()).decode()
    plot_url1 = base64.b64encode(img1.getvalue()).decode()
    plot_url2 = base64.b64encode(img2.getvalue()).decode()
    out = "data:image/png;base64,{}".format(plot_url)
    out1 = "data:image/png;base64,{}".format(plot_url1)
    out2 = "data:image/png;base64,{}".format(plot_url2)

    list = [out, out1, out2, "Model Performance:", "Forex prediction for the next 3 days:", "Seasonal maximums and minimums from the predictions:"]

    return render_template('predictions.html', graphs=list)



# if __name__ == "__main__":
#     app.run(debug=True, port=5000)