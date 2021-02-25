import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time
a=st.text_input(label='1st Company for Comparision')
b=st.text_input(label='2nd Company for Comparision')
Stocks=[a,b]
if st.button('Collect Data'):
    with st.spinner('Analysis of Stocks...'):
        time.sleep(1)
Stocks_data=yf.download(Stocks,period='2mo')
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


st.plotly_chart(fig_Sharpe)
