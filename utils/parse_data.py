import csv
from datetime import datetime


# parsing historical data, to create real time simulator to test strategies
def parse_historical_data_by_symbol(filename,symbol):
    start = 0
    with open(filename) as file:
        csv_file = csv.reader(file)
        next(csv_file)
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
            if start == 0:
                print("START", ts_event)
                start = ts_event
        end = convert_epoch_time(ts_event)
        print(end)
        start = convert_epoch_time(start)
        print(start)
        print(end - start)

def convert_epoch_time(epoch):
    """
    function will convert the epoch string to time, which will then
    be used to simulate a real time market
    """
    date = datetime.fromisoformat(epoch)
    return date


def main():
    parse_historical_data("../data/processed/dbeq-basic-20241204.ohlcv-1s.csv")


main()
