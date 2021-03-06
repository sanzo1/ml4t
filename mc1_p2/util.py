"""MLT: Utility code."""

import os
import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir=os.path.join("..", "data")):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates, addSPY=True):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price", filename=None):
    """Plot stock prices with game_data custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if filename is not None:
        plt.savefig(filename)
    plt.show()


def plot_normalized_data(df, title="Normalized prices", xlabel="Date", ylabel="Normalized price"):
    normalized_prices = df / df.ix[0]
    plot_data(normalized_prices, title, xlabel, ylabel)
    

def download_data(symbol, dates):
    """Download historical prices from Yahoo Finance website and save
    the data into CSV files."""
    historical = pd.io.data.DataReader(symbol, 'yahoo', dates[0], dates[1])
    historical.to_csv( symbol_to_path(symbol) )        
