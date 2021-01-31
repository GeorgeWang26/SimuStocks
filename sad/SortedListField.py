from mongoengine import Document, connect
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, FloatField, SortedListField, StringField
import json
from flask_login import UserMixin

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

class LoginReturn(Document, UserMixin):
    username = StringField(unique = True, required = True)
    meta = {
        'ordering': ['+username']
    }

class StockInfo(Document):
    allStocks = SortedListField(EmbeddedDocumentField(Stock), ordering = 'name')


def addUser(username, email, password):
    if User.objects(username = username):
        return  'username already exist'
    if User.objects(email = email):
        return 'email address already used'
    user = User(username = username, email = email, password = password)

    #adding everything in the stockinfo into watch list
    #need to make a list of only the default on for init
    allStocks= StockInfo.objects.first().allStocks
    for stock in allStocks:
        user.watchList.append(stock)
    # apple = newStock(apple)
    # use the scrape to get info by name
    # then store the info into watchlist
    # defualt watclist: apple, google, amazon.........
    user.save()
    LoginReturn(username = username).save()
    return 'success'


def authenticate(username, password):
    if '@' in username:
        user = User.objects(email = username).first()
    else:
        user = User.objects(username = username).first()

    if user:
        if user.password == password:
            return LoginReturn.objects(username = user.username).first()
        return 'wrong password'
    return 'no such user'


def getFromId(user_id):
    user = LoginReturn.objects(id=user_id).first()
    if not user:
        return 'no such user id'
    return user









def newStock(symbol, name, price, delta):
    stockInfo = StockInfo.objects().first()
    if stockInfo:
        allStocks = stockInfo.allStocks
        print(allStocks)
        for stock in allStocks:
            if symbol == stock.symbol:
                return 'stock info already exist in db'
        print('adding new stock')
        newStock = Stock(symbol = symbol, name = name, price = price, delta = delta)
        allStocks.append(newStock)
        stockInfo.save()
        return('success')

    else:
        print('first time adding stock, creating new stock list')
        newStockList = StockInfo()
        newStock = Stock(symbol = symbol, name = name, price = price, delta = delta)
        newStockList.allStocks.append(newStock)
        newStockList.save()
        print('first stock added in the liust')
        return('success')
        



def updateAllStockInfo():
    stockInfo = StockInfo.objects().first()
    if not stockInfo:
        return 'empty stock info list'
    allStocks = stockInfo.allStocks
    for stock in allStocks:
        stock.price += 1
    stockInfo.save()
    return('success')



# print(newStock('APL', 'Apple', 2.333, 'delta is here'))
# print(newStock('gll', 'google', 2.22, 'delta is here'))
print(json.dumps(json.loads(StockInfo.objects().to_json()), sort_keys=True, indent=4))


print(addUser('b', 'b-email', 'pass'))
print(addUser('a', 'a-email', 'pass'))
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4))

print(updateAllStockInfo())
print(json.dumps(json.loads(StockInfo.objects().to_json()), sort_keys=True, indent=4))
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4))




User.drop_collection()
LoginReturn.drop_collection()

