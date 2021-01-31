var result = {'stocks': [{'symbol': 'AAPL', 'price': 131.96, 'share': 4, 'value': 527.84}, {'symbol': 'GOOG', 'price': 1835.74, 'share': 3, 'value': 5507.22}], 'totalValue': 6035.06}

var stocks = result.stocks
var totalValue = result.totalValue

for (stock in stocks){
    symbol = stock.symbol
    price = stock.price
    share = stock.share
    value = stock.value
}
