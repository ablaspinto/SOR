
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

    def get_symbols(self):
        return self.__symbols

    def add_trade(self, symbol, amount, timeframe):
        if symbol in self.__volume_amount:
            self.__volume_amount[symbol].append((symbol, amount, timeframe))
        else:
            self.__volume_amount[symbol] = []
            self.__volume_amount[symbol].append((symbol, amount, timeframe))
