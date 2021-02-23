import streamlit as st

st.title('DeepSaRa Stock Guru') 

import pandas as pd
import numpy as np
import yfinance as yf
from nsetools import Nse
nse = Nse()
a=nse.get_top_gainers()
b=pd.DataFrame(a)
c=list(b.symbol+'.NS')

st.markdown('_Top Gainers are the stocks which have increased their Closing Price the most compared to the previous trading sessions_')
st.header('Top Gainers in NSE')
st.table(c)

Gainers=yf.download(c,period='2mo')
Nifty=yf.download('^NSEI',period='2mo')
Data_Close_price=Gainers['Adj Close'].join(Nifty['Adj Close'])
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
              title='Top Gainers Value',width=800,height=600)
fig.add_scatter(x=Predictions_value['index'], y=Predictions_value['Adj Close'],name='NIFTY')
fig.show()

st.markdown('_This chart shows the Performance of each stock compared to the Market performance,i.e. if the chart shows any of the stocks above the dotted line (NSE) then it will perform better then the market in the Future. You can also compare the data in the chart where the options for comparision are present in the Top right corner of the chart_') 
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
fig_Sharpe = go.Figure(data=[go.Bar(
            x=Sharpe_ratio.index, y=Sharpe_ratio[0],
            text=Sharpe_ratio.index,
            textposition='auto'
        )])

fig_Sharpe.show()

st.markdown('_This chart shows the Risk and Return on each of the stock, higher the value more likely are you to recieve returns from that stock, with the risks present in that stock_') 
st.header('Best Stock to invest in according to Risks and Returns rate present in stock')
st.plotly_chart(fig_Sharpe)

Close_Price=Gainers['Adj Close'].iloc[-1,:]
st.header('Price')
st.table(Close_Price)


