import scrape.Stock as Stock
import requests
from bs4 import BeautifulSoup

class PriceCollector:

    def connect(symbol):
        try:
            url = "https://ca.finance.yahoo.com/quote/"+symbol+"?p="+symbol
            return requests.get(url)
        except:
            print()

    def getStock(result):
        try:
            stockInfo = []
            prices = BeautifulSoup(result.content).select("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div > div > span")
            company = BeautifulSoup(result.content).select("#quote-header-info > div> div > div> h1")
            for info in prices:
                stockInfo.append(info.text.strip())
            for info in company:
                text = info.text
                x = text.split("(")
                stockInfo.append(x[0].strip())
                stockInfo.append(x[1].strip().replace(")", ""))
            return Stock(stockInfo[2], stockInfo[3], stockInfo[0], stockInfo[1])
        except:
            print()

