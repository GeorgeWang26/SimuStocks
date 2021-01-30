from mongoengine import Document, connect
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, FloatField, SortedListField, StringField
import json


connect('test')

class Stock(EmbeddedDocument):
    symbol = StringField(required = True)
    name = StringField(required = True)
    price = FloatField(required = True)
    delta = StringField(required = True)


class OwnedStock(EmbeddedDocument):
    symbol = StringField(required = True)
    stock = EmbeddedDocumentField(Stock, required = True)
    shareCount = FloatField(required = True)
    value = FloatField(required = True)


class User(Document):
    username = StringField(required = True, unique = True)
    email = StringField(required = True, unique = True)
    password = StringField(required = True)
    watchList = SortedListField(EmbeddedDocumentField(Stock), ordering = 'symbol')
    balence = FloatField(default = 10000.00)
    ownedStock = SortedListField(EmbeddedDocumentField(OwnedStock), ordering = 'symbol')
    totalStockValue = FloatField(default = 0.00)
    meta = {
        'ordering': ['+username']
    }

class StockInfo(Document):
    allStocks = SortedListField(EmbeddedDocumentField(Stock), ordering = 'name')


def newUser(username, email, password):
    if User.objects(username = username):
        return  'username already exist'
    if User.objects(email = email):
        return 'email address already used'
    user = User(username = username, email = email, password = password)
    # apple = newStock(apple)
    # use the scrape to get info by name
    # then store the info into watchlist
    # defualt watclist: apple, google, amazon.........
    user.save()
    return 'success'

def newStock(symbol, name, price, delta):
    if len(StockInfo.objects()) > 0:
        stockCollector = StockInfo.objects().first()
        print(stockCollector)
        allStocks = stockCollector.allStocks
        for stock in allStocks:
            if symbol == stock.symbol:
                return 'stock info already exist in db'
        print('adding new stock')
        stock = Stock(symbol = symbol, name = name, price = price, delta = delta)
        allStocks.append(stock)
        StockInfo.objects().first().save()
        print('new stock addede')
    else:
        print('first time adding stock, creating new stock list')
        newStockList = StockInfo()
        stock = Stock(symbol = symbol, name = name, price = price, delta = delta)
        newStockList.allStocks.append(stock)
        newStockList.save()
        print('first stock added in the liust')
    return('success')
        
print(newStock('APL', 'Apple', 2.333, 'delta is here'))
# newUser('a', 'a.casda', 'asd')
print(json.dumps(json.loads(StockInfo.objects().to_json()), sort_keys=True, indent=4))

#def updateStockInfo()

# print('hi')
# print(StockInfo.objects())
# allStocks = StockInfo.objects().first().allStocks()
# print(allStocks)
# print('hi again')



