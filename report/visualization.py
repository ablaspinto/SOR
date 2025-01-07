import pandas as pd
import matplotlib.pyplot as plt
import csv
from datetime import datetime


def visualize_market(filename, s_symbol):
    open_d = []
    close_d = []
    high_d = []
    low_d = []
    time = []
    with open(filename) as file:
        csv_file = csv.reader(file)
        fields = next(csv_file)
        for record in csv_file:
            ts_event = record[0]
            r_type = record[1]
            publisher_id = record[2]
            instrument_id = record[3]
            open_price = record[4]
            high = record[5]
            low = record[6]
            close = record[7]
            volume = record[8]
            symbol = record[9]
            if symbol == s_symbol:
                open_d.append(float(open_price))
                close_d.append(float(close))
                high_d.append(float(high))
                low_d.append(float(low))
            time.append(datetime.fromisoformat(ts_event))
    stock_prices = pd.DataFrame(
        {
            'open': open_d,
            'close': close_d,
            'high': high_d,
            'low': low_d,
        },
        index=pd.to_datetime(time[:len(open_d)])
    )

    plt.figure()

    up = stock_prices[stock_prices.close >= stock_prices.open] # up ticks

    down = stock_prices[stock_prices.close < stock_prices.open] # down ticks

    col1 = "red"

    col2 = "green"

# Setting width of candlestick elements
    width = .0005
    width2 = .0001
    plt.bar(up.index, up.close-up.open, width,
            bottom=up.open, color=col1, edgecolor='grey')
    plt.bar(up.index, up.high-up.close, width2,
            bottom=up.close, color=col1, edgecolor='grey')
    plt.bar(up.index, up.low-up.open, width2,
            bottom=up.open, color=col1, edgecolor='grey')

    # Plot down candlesticks
    plt.bar(down.index, down.close-down.open, width,
            bottom=down.open, color=col2, edgecolor='grey')
    plt.bar(down.index, down.high-down.open, width2,
            bottom=down.open, color=col2, edgecolor='grey')
    plt.bar(down.index, down.low-down.close, width2,
            bottom=down.close, color=col2, edgecolor='grey')

    # Improve the appearance of x-axis
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(f'Candlestick Chart for {s_symbol}')
    plt.tight_layout()
    # Show the plot
    plt.show()

def main():
    visualize_market(
        "../data/processed/dbeq-basic-20241204.ohlcv-1s.csv", "AAPL")


main()
