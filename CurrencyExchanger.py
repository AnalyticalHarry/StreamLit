import streamlit as st

#exchange rates
exchange_rates = {'usd': 1.0, 'eur': 0.85,
                  'gbp': 0.73, 'jpy': 112.15,
                  'aud': 1.32, 'cad': 1.28,
                  'inr': 74.94, 'cny': 6.38,
                  'mxn': 20.04}

#function for converting currency
def currency_converter(amount, from_currency, to_currency):
    #print function if currency doesn't exist inside dictionary
    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        st.write("Invalid currency code.")
        return None
    #formula to convert currency
    converted_amount = amount * exchange_rates[to_currency] / exchange_rates[from_currency]
    #return converted amount
    return converted_amount

#simple currency converter
st.write("Welcome to the currency converter!")

#get data from user
amount = st.number_input("Enter the amount:", value=1.0, step=0.01)

from_currency_key = "from_currency_input"
from_currency = st.text_input("Enter the source currency code (e.g., usd):", key=from_currency_key).lower()

to_currency_key = "to_currency_input"
to_currency = st.text_input("Enter the target currency code (e.g., eur):", key=to_currency_key).lower()

#button for performing conversion
if st.button("Convert"):
    #performing conversion rate
    result = currency_converter(amount, from_currency, to_currency)

    #display the result
    if result is not None:
        st.write(f"{amount} {from_currency} is equal to {result:.2f} {to_currency}.")
