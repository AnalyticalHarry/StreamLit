
# Importing Libraries
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# creating function to fetch dataset
@st.cache_data
def fetch_data(tickers, start_date, end_date):
    data = {}
    for ticker_name, ticker_symbol in tickers.items():
        data[ticker_name] = yf.download(ticker_symbol, start=start_date, end=end_date)
    return data

# function to plot volume and price 
def plot_indices_volume_and_price(data1, data2, label1, label2):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data1.index, y=data1['Volume'], name=f'{label1} Volume', marker_color='red'))
    fig.add_trace(go.Bar(x=data2.index, y=data2['Volume'], name=f'{label2} Volume', marker_color='blue'))

    fig.add_trace(go.Scatter(x=data1.index, y=data1['Adj Close'], name=f'{label1} Adj Close', yaxis='y2', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=data2.index, y=data2['Adj Close'], name=f'{label2} Adj Close', yaxis='y2', line=dict(color='blue')))

    fig.update_layout(
        title='Indices Volume and Adjusted Close Price Analysis',
        yaxis=dict(title='Volume'),
        yaxis2=dict(title='Adj Close Price', overlaying='y', side='right'),
        xaxis=dict(
            tickmode='linear',
            tick0=data1.index[0],
            dtick='M12'
        ),
        showlegend=True
    )
    return fig

#function to plot volume correlation
def plot_volume_correlation(data1, data2, ticker1, ticker2, degree=1):
    df = pd.DataFrame({
        f"{ticker1} Volume": data1['Volume'],
        f"{ticker2} Volume": data2['Volume']
    })

    fig = px.scatter(df, x=f"{ticker1} Volume", y=f"{ticker2} Volume", trendline="ols",
                     title=f'Volume Correlation: {ticker1} vs. {ticker2}',
                     color_discrete_sequence=['red'],
                     opacity=0.5)

    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey'), symbol='square', size=5))

    correlation_volume = data1['Volume'].corr(data2['Volume'])
    fig.add_annotation(text=f'Volume Correlation: {correlation_volume:.2f}',
                        xref="paper", yref="paper", x=0.05, y=0.95, showarrow=False)

    poly_features = PolynomialFeatures(degree=degree)
    X = data1['Volume'].values.reshape(-1, 1)
    y = data2['Volume'].values
    X_poly = poly_features.fit_transform(X)
    model = LinearRegression()
    model.fit(X_poly, y)
    X_fit = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)  
    y_fit = model.predict(poly_features.transform(X_fit))
    fig.add_trace(go.Scatter(x=X_fit.squeeze(), y=y_fit, mode='lines', name=f'Regression (Degree {degree})', line=dict(color='blue')))
    return fig

#function to train and plot linear regression model
def train_and_plot_linear_regression(data1, data2, ticker1, ticker2, degree=3, test_size=0.2):
    adj_close1 = data1['Adj Close'].values.reshape(-1, 1)
    adj_close2 = data2['Adj Close'].values
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(adj_close1)  
    X_train, X_test, y_train, y_test = train_test_split(X_poly, adj_close2, test_size=test_size, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_poly)  
    y_pred_test = model.predict(X_test)
    test_df = pd.DataFrame({
        f"{ticker1} Adj Close": X_test[:, 1],
        f"{ticker2} Adj Close": y_test
    })
    test_df = test_df.sort_values(by = f"{ticker1} Adj Close")
    fit_df = pd.DataFrame({
        f"{ticker1} Adj Close": adj_close1.flatten(),
        "Predicted Adj Close": y_pred
    })
    fit_df = fit_df.sort_values(by = f"{ticker1} Adj Close")

    fig = px.scatter(test_df, x=f"{ticker1} Adj Close", y=f"{ticker2} Adj Close",
                     title=f'Adj Close Price Regression: {ticker1} vs. {ticker2} (Degree {degree}, Test Size {test_size*100:.0f}%)',
                     color_discrete_sequence=['red'],
                     opacity=0.5)
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey'), symbol='square', size=5))
    fig.add_trace(go.Scatter(x=fit_df[f"{ticker1} Adj Close"], y=fit_df["Predicted Adj Close"],
                             mode='lines', name='Best Fit Line', line=dict(color='blue')))
    r2 = r2_score(adj_close2, y_pred) 
    fig.add_annotation(text=f'R-squared: {r2:.2f}',
                        xref="paper", yref="paper", x=0.05, y=0.85, showarrow=False)
    return fig

#function to run all function using common function
def main():
    st.title("Correlation Analysis")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime(datetime.today().strftime('%Y-%m-%d')))
    ticker1 = st.text_input("Enter the first ticker symbol (e.g., SPY, NVDA, MSFT):", "SPY")
    ticker2 = st.text_input("Enter the second ticker symbol (e.g., DIA, GOOG, AAPL):", "DIA")
    tickers = {ticker1: ticker1, ticker2: ticker2}
    data = fetch_data(tickers, start_date, end_date)
    test_size = st.slider("Select Test Set Size", min_value=0.1, max_value=0.5, value=0.2, step=0.05)
    fig1 = plot_indices_volume_and_price(data[ticker1], data[ticker2], ticker1, ticker2)
    degree = st.slider("Select Polynomial Degree for Volume Correlation and Regression", min_value=1, max_value=5, value=1)
    fig2 = plot_volume_correlation(data[ticker1], data[ticker2], ticker1, ticker2, degree=degree)
    fig3 = train_and_plot_linear_regression(data[ticker1], data[ticker2], ticker1, ticker2, degree=degree, test_size=test_size)
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
main()
