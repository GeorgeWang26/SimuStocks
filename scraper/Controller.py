from sys import exec_prefix
from PriceCollector import PriceCollector


while True:
    try:
        stock = input("\nEnter a stock: ")
        if(stock == "0"):
            break
        print(1)
        src = PriceCollector.connect(stock)
        print(2)
        if(src.status_code == 200):
            print("\n\n\n" + PriceCollector.getStock(src).toString())
        else:
            print("Error finding stock")
    except:
        print("Error Finding Stock")

print("EXIT")