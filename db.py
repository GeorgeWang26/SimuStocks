from mongoengine import Document, connect
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, FloatField, IntField, ListField, SortedListField, StringField
import json
from flask_login import UserMixin

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



# def addNewStock(symbol):
#     #use scraper
#     newStock()


def newStock(symbol, name, price, change):
    if Stocks.objects(symbol = symbol).first():
        return 'stock already exist'
    Stocks(symbol = symbol, name = name, price = price, change = change).save()
    return 'success'



def updateAllStockInfo():
    stocks = Stocks.objects()
    for stock in stocks:
        #use scrape to update info
        stock.price = (stock.price + 1)  #(new price)
        stock.change = 'updated change' #(new change)
        stock.save()
    return('success')



def addToWatchList(username, symbol):

# add this in !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # if not Stocks.objects(symbol = symbol).first():
    #     addNewStock()

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
    user = User.objects(username = username).first()
    for i in range(len(user.watchList)):
        if user.watchList[i].symbol == symbol:
            user.watchList.pop(i)
            user.save()
            return('success')
    return ('stock not found')



def buyStock(username, symbol, share):
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










User.drop_collection()
LoginReturn.drop_collection()
Stocks.drop_collection()
print(json.dumps(json.loads(Stocks.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')

newStock('apl', 'apple', 200 ,'change')
newStock('DICK', 'dick org', 1000000, 'change')
newStock('gll', 'Goglle', 1, 'change')
addUser('a', 'email', 'pass')
addToWatchList('a','apl')
addToWatchList('a','gll')
addToWatchList('a', 'DICK')

print(json.dumps(json.loads(Stocks.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')


print('start buying----------------------------------------------------------------------------------------------')
print(buyStock('a','DICK', 1))
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
print(buyStock('a','apl',3))
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
print('start selling----------------------------------------------------------------------------------------------')
print(sellStock('a', 'gll', 9))
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')

print(sellStock('a', 'apl', 3))
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')

print(buyStock('a','apl',3))
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')

# print('----------------------------------------------------------------------------------------------')
# print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
# print(removeFromWatchList('a', 'apl'))
# print(removeFromWatchList('a', 'asdsad'))
# print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')



