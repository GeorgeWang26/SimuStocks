from sys import exec_prefix
import PriceCollector



def getStockInfo(symbol):
    try:

        src = PriceCollector.connect(symbol)
        if(src.status_code == 200):
            return PriceCollector.getStock(src)
        else:
            return("invalid stock symbol")
    except:
        print("some really bad bad things happened")


if __name__ == '__main__':    
    stock = getStockInfo('amzn')
    print(stock)
    print(stock.name, stock.symbol, type (stock.price),stock.price, stock.change)
