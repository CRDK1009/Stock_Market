import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time
st.title('DeepSaRa Stock Guru') 
st.markdown("_Fill all Companies' names (Company Stock Symbols) with the Suffix as '.NS' and fill it as Uppercase letters_")
st.markdown("_Please fill all the Values for the App to continue functioning_")
st.markdown("_Example:_")
st.markdown("_LT.NS_")
st.markdown("_BHEL.NS_")
st.markdown("_The above example shows the Symbol of Larsen & Toubro and Bharat Heavy Electricals Limited respectively. These symbols represent them in the Stock market_")
a=st.text_input(label='1st Company for Comparision')
b=st.text_input(label='2nd Company for Comparision')
Stocks=[a,b]
Stocks_data=yf.download(Stocks,period='2mo')
st.markdown("_A snippet of the data collected_")
st.table(Stocks_data['Adj Close'].head())
Nifty=yf.download('^NSEI',period='2mo')
Data_Close_price=Stocks_data['Adj Close'].join(Nifty['Adj Close'])
Value=Data_Close_price.pct_change()
from statsmodels.tsa.statespace.varmax import VARMAX
# fit model
model = VARMAX(Value, order=(1, 1))
model_fit = model.fit(disp=False)
# make prediction
yhat_value = model_fit.forecast(steps=7,n_jobs=-1)
Predictions_value=pd.DataFrame(yhat_value)
Predictions_value=Predictions_value.reset_index()
import plotly.express as px
fig = px.line(Predictions_value, x="index", y=Predictions_value.drop(['Adj Close'],axis=1).columns,
              title='Value of Stocks')
fig.add_scatter(x=Predictions_value['index'], y=Predictions_value['Adj Close'],name='NIFTY')
st.markdown('_This chart below shows the Performance of each stock compared to the Market performance,i.e. if the chart shows any of the stocks above the dotted line (NSE) then it will perform better than the market in the Future. You can also compare the data in the chart where the options for comparision are present in the Top right corner of the chart_') 
st.plotly_chart(fig)
stock_returns=Value.drop(['Adj Close'],axis=1)
sp_returns=Value['Adj Close']
excess_returns=stock_returns.sub(sp_returns,axis=0)
avg_excess_return=excess_returns.mean()
sd_excess_return=excess_returns.std()
daily_sharpe_ratio=avg_excess_return.div(sd_excess_return)
annual_factor=np.sqrt(252)
annual_sharpe_ratio=daily_sharpe_ratio.mul(annual_factor)
Sharpe_ratio=pd.DataFrame(annual_sharpe_ratio)
import plotly.graph_objects as go
# Use textposition='auto' for direct text
fig_Sharpe = go.Figure(data=[go.Bar(
            x=Sharpe_ratio.index, y=Sharpe_ratio[0],
            text=Sharpe_ratio.index,
            textposition='auto',
        )])

st.markdown('_This chart below shows the Risk and Return on each of the stock, higher the value more likely are you to recieve returns from that stock, with the risks present in that stock_') 
st.header('Best Stock to invest in according to Risks and Returns rate present in stock')
st.plotly_chart(fig_Sharpe)
Close_Price=Stocks_data['Adj Close'].iloc[-1,:]
st.header('Price')
st.table(Close_Price)
st.markdown("_~ C R Deepak Kumar_")
