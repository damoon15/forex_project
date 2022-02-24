import pickle
import yfinance as yf
from datetime import datetime,timedelta




#%%load_model

#with open ('./model_sarima.pkl', 'rb') as file:
    #model = pickle.load(file)

#%%Download JPYAUD data
data = yf.download(tickers = 'JPYAUD=X' ,period ='10mo', interval = '1d')

def toDate(dateString):
    return datetime.strptime(dateString, "%Y-%m-%d").date()

if __name__=='__main__':
    model.summary()



