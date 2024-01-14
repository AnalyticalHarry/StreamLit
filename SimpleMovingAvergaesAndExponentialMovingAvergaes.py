#pip install yfinance plotly
import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import base64
from datetime import datetime, timedelta
import io  
import os  

def download_csv_button(data, filename, button_text="Download CSV"):
    csv_file = io.StringIO()
    #set index=True to include the date column
    data.to_csv(csv_file, index=True)  
    csv_file.seek(0)
    
    b64_csv = base64.b64encode(csv_file.read().encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64_csv}" download="{filename}.csv">{button_text}</a>'
    return href

st.title("Simple Moving Avergaes and Exponential Moving Averages Analysis")

#get user input for stock ticker
ticker = st.text_input("Enter stock ticker symbol (e.g., AAPL):").upper()

#select box for predefined time intervals
time_interval_options = ["1 Day", "2 Days", "3 Days", "6 Months", "1 Year", "2 Years", "3 Years", "4 Years", "5 Years", "10 Years", "Custom"]
selected_time_interval = st.selectbox("Select time interval:", time_interval_options)

#if "Custom" is selected, allow the user to input a custom end date
if selected_time_interval == "Custom":
    start_date = st.date_input("Select start date:", datetime(2022, 1, 1))
    end_date = st.date_input("Select end date:", datetime.today())
else:
    #start and end dates based on the selected interval
    end_date = datetime.today()
    if selected_time_interval == "1 Day":
        start_date = end_date - timedelta(days=1)
    elif selected_time_interval == "2 Days":
        start_date = end_date - timedelta(days=2)
    elif selected_time_interval == "3 Days":
        start_date = end_date - timedelta(days=3)
    elif selected_time_interval == "6 Months":
        start_date = end_date - timedelta(days=6 * 30)
    elif selected_time_interval == "1 Year":
        start_date = end_date - timedelta(days=365)
    elif selected_time_interval == "2 Years":
        start_date = end_date - timedelta(days=2 * 365)
    elif selected_time_interval == "3 Years":
        start_date = end_date - timedelta(days=3 * 365)
    elif selected_time_interval == "4 Years":
        start_date = end_date - timedelta(days=4 * 365)
    elif selected_time_interval == "5 Years":
        start_date = end_date - timedelta(days=5 * 365)
    elif selected_time_interval == "10 Years":
        start_date = end_date - timedelta(days=10 * 365)

#user input for the number of SMA and EMA periods
num_sma_periods = st.number_input("Enter the number of Simple Moving Average (SMA) periods:", min_value=0, max_value=10, value=2)
num_ema_periods = st.number_input("Enter the number of Exponential Moving Average (EMA) periods:", min_value=0, max_value=10, value=2)

#user input for SMA periods
if num_sma_periods > 0:
    sma_periods = [st.number_input(f"Enter SMA period {i + 1}:", min_value=1, max_value=100, value=20) for i in range(num_sma_periods)]
else:
    sma_periods = []

#user input for EMA periods
if num_ema_periods > 0:
    ema_periods = [st.number_input(f"Enter EMA period {i + 1}:", min_value=1, max_value=100, value=12) for i in range(num_ema_periods)]
else:
    ema_periods = []

#button for fetching and plotting data
if st.button("Plot Stock Data"):
    #fetch historical stock data
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if stock_data.empty:
        st.write(f"No historical stock price data available for {ticker}. Please check the ticker symbol and date range.")
    else:
        #SMA and EMA
        for i in range(num_sma_periods):
            stock_data[f'SMA{i + 1}'] = stock_data['Close'].rolling(window=sma_periods[i]).mean()

        for i in range(num_ema_periods):
            stock_data[f'EMA{i + 1}'] = stock_data['Close'].ewm(span=ema_periods[i], adjust=False).mean()

        #plotting stock data with SMA and EMA
        sma_labels = [f'SMA{i + 1}' for i in range(num_sma_periods)]
        ema_labels = [f'EMA{i + 1}' for i in range(num_ema_periods)]

        all_labels = ['Close'] + sma_labels + ema_labels

        fig = px.line(stock_data, x=stock_data.index, y=all_labels,
                      labels={'Close': 'Stock Price'},
                      title=f'{ticker} Stock Price Over Time with SMA and EMA')
        st.plotly_chart(fig)

        #button for downloading plotted data in CSV format
        download_button_text = f"Download {ticker} Plotted Data (CSV)"
        st.markdown(download_csv_button(stock_data, f"{ticker}_plotted_data", button_text=download_button_text), unsafe_allow_html=True)
