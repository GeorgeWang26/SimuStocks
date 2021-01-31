from mongoengine import Document, connect
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, FloatField, SortedListField, StringField, EmbeddedDocumentListField
import json
from flask_login import UserMixin

connect('test')

class Stock(Document):
    symbol = StringField(required = True)
    name = StringField(required = True)
    price = FloatField(required = True)
    delta = StringField(required = True)


# class OwnedStock(EmbeddedDocument):
#     symbol = StringField(required = True)
#     stock = EmbeddedDocumentField(Stock)
#     shareCount = FloatField(required = True)
#     value = FloatField(required = True)


class User(Document):
    username = StringField(required = True, unique = True)
    email = StringField(required = True, unique = True)
    password = StringField(required = True)
    watchList = EmbeddedDocumentListField(Stock)
    balence = FloatField(default = 10000.00)
    # ownedStock = EmbeddedDocumentListField(OwnedStock)
    totalStockValue = FloatField(default = 0.00)
    meta = {
        'ordering': ['+username']
    }

class LoginReturn(Document, UserMixin):
    username = StringField(unique = True, required = True)
    meta = {
        'ordering': ['+username']
    }



def addUser(username, email, password):
    if User.objects(username = username):
        return  'username already exist'
    if User.objects(email = email):
        return 'email address already used'
    user = User(username = username, email = email, password = password)

    #adding everything in the stockinfo into watch list
    #need to make a list of only the default on for init
    
    for stock in Stock.objects():
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
    if Stock.objects(symbol = symbol).first():
        return 'stock already exist'
    Stock(symbol = symbol, name = name, price = price, delta = delta).save()



def updateAllStockInfo():
    for stock in Stock.objects():
        stock.price = stock.price+1
    return 'success'



newStock('app','apple',1,'change')
addUser('a', 'a-email', 'pass')
updateAllStockInfo()
addUser('b','n-email','pass')
print(json.dumps(json.loads(Stock.objects().to_json()), sort_keys=True, indent=4))
print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4))