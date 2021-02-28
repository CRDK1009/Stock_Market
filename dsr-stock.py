import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import time
import plotly.graph_objects as go
st.title('DeepSaRa Stock Guru') 
st.markdown("_Fill all Companies' names (Company Stock Symbols) with the Suffix as '.NS' and fill it as Uppercase letters_")
st.markdown("_Please fill all the Values for the App to continue functioning_")
st.markdown("_Example:_")
st.markdown("_LT.NS_")
st.markdown("_BHEL.NS_")
st.markdown("_The above example shows the Symbol of Larsen & Toubro and Bharat Heavy Electricals Limited respectively. These symbols represent them in the Stock market_")
a=st.text_input(label='1st Company for Comparision')
b=st.text_input(label='2nd Company for Comparision')
c=st.text_input(label='3rd Company for Comparision')
d=st.text_input(label='4th Company for Comparision')
e=st.text_input(label='5th Company for Comparision')
Stocks=[a,b,c,d,e]
Stocks_data=yf.download(Stocks,period='2mo')
st.markdown("_A snippet of the data collected_")
st.table(Stocks_data['Adj Close'].head())
Nifty=yf.download('^NSEI',period='2mo')
Data_Close_price=Stocks_data['Adj Close'].join(Nifty['Adj Close'])
Value=Data_Close_price.pct_change()
Nifty_Value=Nifty['Adj Close'].pct_change()
Nifty_Value=pd.DataFrame(Nifty_Value)
Nifty_Value=Nifty_Value.reset_index()
st.markdown("_Value of the market for the past two months_")
import plotly.express as px
fig = px.line(Nifty_Value, x="Date", y=Nifty_Value['Adj Close'],
              title='Value of Market')
st.plotly_chart(fig)
stock_returns=Value.drop(['Adj Close'],axis=1)
sp_returns=Value['Adj Close']
excess_returns=stock_returns.sub(sp_returns,axis=0)
avg_excess_return=excess_returns.mean()
Returns=pd.DataFrame(avg_excess_return)
st.markdown("_Returns in the Stocks_")
fig_Return = go.Figure(data=[go.Bar(
            x=Returns.index, y=Returns[0],
            text=Returns.index,
            textposition='auto',
        )])
st.plotly_chart(fig_Return)
sd_excess_return=excess_returns.std()
Risk=pd.DataFrame(sd_excess_return)
st.markdown("_Risk in the Stocks_")
fig_Risk = go.Figure(data=[go.Bar(
            x=Risk.index, y=Risk[0],
            text=Risk.index,
            textposition='auto',
        )])
st.plotly_chart(fig_Risk)
daily_sharpe_ratio=avg_excess_return.div(sd_excess_return)
annual_factor=np.sqrt(252)
annual_sharpe_ratio=daily_sharpe_ratio.mul(annual_factor)
Sharpe_ratio=pd.DataFrame(annual_sharpe_ratio)
st.markdown("_Investment Value (Return/Risk) in the Stocks_")
# Use textposition='auto' for direct text
fig_Sharpe = go.Figure(data=[go.Bar(
            x=Sharpe_ratio.index, y=Sharpe_ratio[0],
            text=Sharpe_ratio.index,
            textposition='auto',
        )])


st.plotly_chart(fig_Sharpe)
Close_Price=Stocks_data['Adj Close'].iloc[-1,:]
st.header('Price')
st.table(Close_Price)
st.markdown("_~ C R Deepak Kumar_")
