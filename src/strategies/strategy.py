
class Strategy:
    """
    Parent class fields will be a
    base for the different strategies.
    with priority of expanding into more
    strategies
    """
    __slots__ = ["__name", "__volume_amount", "__symbols"]

    def __init__(self, name):
        # name of strategy and map symbols for volume, for multi leg possibilities
        self.__name = name
        self.__volume_amount = dict()

    def get_name(self):
        return self.__name

    def get_volume_amount(self):
        return self.__volume_amount

    def add_trade(self, symbol, amount, timeframe, execution_price, actual_price):
        if symbol in self.__volume_amount:
            self.__volume_amount[symbol].append(
                (id, symbol, amount, timeframe, execution_price, actual_price))
        else:
            self.__volume_amount[symbol] = []
            self.__volume_amount[symbol].append(
                (id, symbol, amount, timeframe, execution_price, actual_price))

            # {"AAPL": [(1010000023,AAPL,200, 12:34, 50.43, 50.45) , ... ]}

    def get_slippage(self, symbol, id):
        trades = self.__volume_amount[symbol]
        for tup in trades:
            if tup[0] == id:
                return int(tup[5]) - int(tup[4])
