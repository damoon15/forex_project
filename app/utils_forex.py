import pickle
import yfinance as yf




#%%load_model

with open ('./model_sarima.pkl', 'rb') as file:
    model = pickle.load(file)

#%%Download JPYAUD data
data = yf.download(tickers = 'JPYAUD=X' ,period ='10mo', interval = '1d')



if __name__=='__main__':
    model.summary()



