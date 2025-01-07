from "../report/visualization.py" import visualize_market

def main():
    """
    Market Visualizer for AAPL stock
    """
    visualize_market(
        "../data/processed/dbeq-basic-20241204.ohlcv-1s.csv", "AAPL")




main()
