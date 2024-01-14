#pip install forex-python yfinance plotly
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

#function for converting currency
def currency_converter(amount, from_currency, to_currency):
    #download historical exchange rate data
    exchange_rate = yf.download(f'{from_currency}{to_currency}=X', period="10y")['Adj Close']
    #check if the DataFrame is empty
    if exchange_rate.empty:
        st.write(f"No historical exchange rate data available for {from_currency}/{to_currency}.")
        return None

    #converted amount based on the last available exchange rate
    converted_amount = amount * exchange_rate.iloc[-1]
    return converted_amount


st.title("Online Currency Converter")
#get data from user
amount = st.number_input("Enter the amount:", value=1.0, step=0.01)
from_currency = st.selectbox("Select source currency:", ['EUR', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 'SEK', 'CHF', 'ISK', 'NOK', 'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'INR', 'KRW', 'MXN', 'MYR', 'NZD', 'PHP', 'SGD', 'THB', 'ZAR'])
to_currency = st.selectbox("Select target currency:", ['EUR', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 'SEK', 'CHF', 'ISK', 'NOK', 'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'INR', 'KRW', 'MXN', 'MYR', 'NZD', 'PHP', 'SGD', 'THB', 'ZAR'])

#button for performing conversion
if st.button("Convert"):
    #performing conversion
    result = currency_converter(amount, from_currency, to_currency)
    #check if the result is not None before displaying it
    if result is not None:
        st.write(f"{amount} {from_currency} is equal to {result:.2f} {to_currency}.")
        #fetching historical exchange rate data
        exchange_rate = yf.download(f'{from_currency}{to_currency}=X', period="10y")['Adj Close']
        #creating a line plot
        df_plot = pd.DataFrame({'Date': exchange_rate.index, 'Exchange Rate': exchange_rate.values})
        fig = px.line(df_plot, x='Date', y='Exchange Rate',
                      labels={'Exchange Rate': f'{from_currency}/{to_currency}', 'Date': 'Date'},
                      title=f'Historical Exchange Rate ({from_currency}/{to_currency})',
                      )
        st.plotly_chart(fig)
