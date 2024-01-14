#pip install forex-python
import streamlit as st
from forex_python.converter import CurrencyRates

#function for converting currency
def currency_converter(amount, from_currency, to_currency):
    c = CurrencyRates()
    exchange_rate = c.get_rate(from_currency, to_currency)
    converted_amount = amount * exchange_rate
    return converted_amount

#title on web screen
st.title("Live Currency Converter")

#get data from user
amount = st.number_input("Enter the amount:", value=1.0, step=0.01)

from_currency = st.selectbox("Select source currency:", ['EUR', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 'SEK', 'CHF', 'ISK', 'NOK', 'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'INR', 'KRW', 'MXN', 'MYR', 'NZD', 'PHP', 'SGD', 'THB', 'ZAR'])

to_currency = st.selectbox("Select target currency:", ['EUR', 'JPY', 'BGN', 'CZK', 'DKK', 'GBP', 'HUF', 'PLN', 'RON', 'SEK', 'CHF', 'ISK', 'NOK', 'TRY', 'AUD', 'BRL', 'CAD', 'CNY', 'HKD', 'IDR', 'INR', 'KRW', 'MXN', 'MYR', 'NZD', 'PHP', 'SGD', 'THB', 'ZAR'])

#button for performing conversion
if st.button("Convert"):
    #performing conversion
    result = currency_converter(amount, from_currency, to_currency)

    #display on the result
    st.write(f"{amount} {from_currency} is equal to {result:.2f} {to_currency}.")
