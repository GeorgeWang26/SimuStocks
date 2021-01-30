class Stock:

    def __init__(self, name, symbol, price ,change):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.change = change
    
    def toString(self):
        return self.name + "\n" + self.symbol +  "\n" + self.price + "\n" + self.change

