from mongoengine import Document, connect
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, FloatField, IntField, ListField, SortedListField, StringField
import json
from flask_login import UserMixin
import Controller as scrape



bigNames = ['aapl','goog','amzn']


connect('test')

class Stocks(Document):
    symbol = StringField()
    name = StringField()
    price = FloatField()
    change = StringField()


class OwnedStock(EmbeddedDocument):
    symbol = StringField()
    share = IntField()

class WatchStock(EmbeddedDocument):
    symbol = StringField()


class User(Document):
    username = StringField()
    email = StringField()
    password = StringField()
    balence = FloatField(default = 10000.00)
    totalStockValue = FloatField(default = 0.00)

    # watchList = SortedListField(EmbeddedDocumentField(WatchStock), ordering = 'symbol')
    watchList = ListField(EmbeddedDocumentField(WatchStock))
    ownedStock = ListField(EmbeddedDocumentField(OwnedStock))
    meta = {
        'ordering': ['+username']
    }

class LoginReturn(Document, UserMixin):
    username = StringField()




def addUser(username, email, password):
    if User.objects(username = username):
        return  'username already exist'
    if User.objects(email = email):
        return 'email address already used'
    User(username = username, email = email, password = password).save()
    LoginReturn(username = username).save()

    for i in bigNames:
        addToWatchList(username, i)

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



def newStock(symbol):
    symbol = symbol.upper()
    if Stocks.objects(symbol = symbol).first():
        return 'stock already exist'
    stock = scrape.getStockInfo(symbol)
    if type(stock) == str or stock == None:
        return 'invalid stock symbol'
    Stocks(symbol = stock.symbol, name = stock.name, price = stock.price, change = stock.change).save()
    return 'success'



# def newStock(symbol, name, price, change):
#     if Stocks.objects(symbol = symbol).first():
#         return 'stock already exist'
#     Stocks(symbol = symbol, name = name, price = price, change = change).save()
#     return 'success'




def updateAllStockInfo():
    stocks = Stocks.objects()
    for stock in stocks:
        symbol = stock.symbol
        info = scrape.getStockInfo(symbol)
        stock.price = info.price
        stock.change = info.change
        stock.save()
    return('success')



def addToWatchList(username, symbol):
    symbol = symbol.upper()
    if not Stocks.objects(symbol = symbol).first():
        print('add new stock from addingtowatchlist')
        print(newStock(symbol = symbol))
        
    user = User.objects(username = username).first()
    watchList = user.watchList
    for stock in watchList:
        if stock.symbol == symbol:
            return 'stock already watched'
    newStockWatched = WatchStock(symbol = symbol)
    user.watchList.append(newStockWatched)
    user.save()
    return('success')




def removeFromWatchList(username, symbol):
    symbol = symbol.upper()
    user = User.objects(username = username).first()
    for i in range(len(user.watchList)):
        if user.watchList[i].symbol == symbol:
            user.watchList.pop(i)
            user.save()
            return('success')
    return ('stock not found')



def getWatchList(username):
    user = User.objects(username = username).first()
    stocks = []
    for i in user.watchList:
        symbol = i.symbol
        # print(symbol)
        stock = Stocks.objects(symbol = symbol).first()
        temp = {}
        temp['symbol'] = symbol
        temp['price'] = stock.price
        temp['change'] = stock.change
        stocks.append(temp)
    return stocks





def buyStock(username, symbol, share):
    symbol = symbol.upper()
    cost = Stocks.objects(symbol = symbol).first().price * share
    user = User.objects(username = username).first()

    if cost > user.balence:
        return 'dont have enough balence'
    else:
        user.balence -= cost

    for stock in user.ownedStock:
        if stock.symbol == symbol:
            stock.share += share
            user.save()
            return('success')

    newShare = OwnedStock(symbol = symbol, share = share)
    user.ownedStock.append(newShare)
    user.save()
    return('success')




def sellStock(username, symbol, share):
    symbol = symbol.upper()
    profit = Stocks.objects(symbol= symbol).first().price * share
    user = User.objects(username = username).first()
    
    for i in range(len(user.ownedStock)):
        stock = user.ownedStock[i]
        
        if stock.symbol == symbol:
            if stock.share < share:
                return 'dont have enough shares to sell'
            else:
                user.balence += profit
                stock.share -= share      #need to check if its chanegd right away
                if stock.share == 0:
                    user.ownedStock.pop(i)
                user.save()
                return 'success'
    return 'stock not found'



def getOwnedStock(username):
    user = User.objects(username = username).first()
    totalValue = 0
    stocks = []
    for i in user.ownedStock:
        symbol = i.symbol
        share = i.share
        price = Stocks.objects(symbol = symbol).first().price
        value = share * price
        totalValue += value
        temp = {}
        temp['symbol'] = symbol
        temp['price'] = price
        temp['share'] = share
        temp['value'] = value
        stocks.append(temp)
    result = {'stocks': stocks, totalValue: totalValue}
    return result





if __name__ == '__main__':

    User.drop_collection()
    LoginReturn.drop_collection()
    Stocks.drop_collection()
    print(json.dumps(json.loads(Stocks.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
    print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')

    addUser('a','email','pass')
    print(json.dumps(json.loads(Stocks.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
    print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')

    print(getWatchList('a'))
    
    buyStock('a', 'aapl', 3)
    buyStock('a', 'goog', 3)
    buyStock('a', 'aapl', 1)
    buyStock('a', 'amzn', 2)
    # 4apple 3google 2amazon
    print()




    User.drop_collection()
    LoginReturn.drop_collection()
    Stocks.drop_collection()