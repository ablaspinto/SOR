import strategy


class TWAP(strategy.Strategy):
    def __init__(self, name):
        super().__init__(name)

def main():
    t = TWAP("TWAP")
    print(t.get_volume_amount())
    print(t.get_name())

main()
