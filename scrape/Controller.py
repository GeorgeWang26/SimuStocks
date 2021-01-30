from sys import exec_prefix
import scrape.PriceCollector as PriceCollector


while True:
    try:
        stock = input("\nEnter a stock: ")
        if(stock == "0"):
            break
        src = PriceCollector.connect(stock)
        if(src.status_code == 200):
            print("\n\n\n" + PriceCollector.getStock(src).toString())
        else:
            print("Error finding stock")
    except:
        print("Error Finding Stock")

print("EXIT")