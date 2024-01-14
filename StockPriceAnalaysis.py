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

st.title("stock Price Analaysis")

#get user input for stock ticker
ticker = st.text_input("Enter stock ticker symbol (e.g., AAPL):").upper()

#selectbox for predefined time intervals
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

#button for fetching and plotting data
if st.button("Plot Stock Data"):
    # Fetch historical stock data
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if stock_data.empty:
        st.write(f"No historical stock price data available for {ticker}. Please check the ticker symbol and date range.")
    else:
        #plotting stock data
        fig = px.line(stock_data, x=stock_data.index, y='Close', labels={'Close': 'Stock Price'}, title=f'{ticker} Stock Price Over Time')
        st.plotly_chart(fig)

        #button for downloading plotted data in CSV format
        download_button_text = f"Download {ticker} Plotted Data (CSV)"
        st.markdown(download_csv_button(stock_data, f"{ticker}_plotted_data", button_text=download_button_text), unsafe_allow_html=True)
