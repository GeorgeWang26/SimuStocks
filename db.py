from mongoengine import Document, connect
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, FloatField, ListField, SortedListField, StringField, EmbeddedDocumentListField
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
    shareCount = FloatField()

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
    # ownedStock = EmbeddedDocumentListField(EmbeddedDocumentField(OwnedStock))
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
    user = User.objects(username = username).first()
    watchList = user.watchList
    for stock in watchList:
        if stock.symbol == symbol:
            return 'stock already watched'
    newStock = WatchStock(symbol = symbol)
    user.watchList.append(newStock)
    user.save()
    return('success')

User.drop_collection()
LoginReturn.drop_collection()
Stocks.drop_collection()
print(json.dumps(json.loads(Stocks.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')


newStock('apl', 'Apple', 1, 'change is here')
newStock('gll', 'Google', 1, 'change is here')
print(json.dumps(json.loads(Stocks.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')


# print(addUser('b', 'b-email', 'pass'))
# print(addToWatchList('b','2'))
# print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
# print(addToWatchList('b', '1'))
# print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')

print(updateAllStockInfo())

# addUser('a', 'a-email', 'pass')
# addToWatchList('a', 'gll')
# addToWatchList('a','apl')

print('price changed\n\n', json.dumps(json.loads(Stocks.objects().to_json()), sort_keys=True, indent=4), '\n\n\n')
# print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4))


# User.drop_collection()
# LoginReturn.drop_collection()
# Stocks.drop_collection()

