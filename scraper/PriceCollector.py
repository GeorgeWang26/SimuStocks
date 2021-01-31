from Stock import Stock
import requests
from bs4 import BeautifulSoup

def connect(symbol):
    try:
        print('tryuing to reach url')
        url = "https://ca.finance.yahoo.com/quote/"+symbol+"?p="+symbol
        return requests.get(url)
    except:
        print()

def getStock(result):
    try:
        stockInfo = []
        prices = BeautifulSoup(result.content).select("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div > div > span")
        company = BeautifulSoup(result.content).select("#quote-header-info > div> div > div> h1")
        # print('hi')
        for info in prices:
            stockInfo.append(info.text.strip())
        # print('hi2.0')
        for info in company:
            text = info.text
            x = text.split("(")
            stockInfo.append(x[0].strip())
            stockInfo.append(x[1].strip().replace(")", ""))
        # print('hi3.0')

        return Stock(stockInfo[2], stockInfo[3], stockInfo[0], stockInfo[1])
    except:
        print()

