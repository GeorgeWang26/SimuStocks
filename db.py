from mongoengine import Document, connect
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, FloatField, SortedListField, StringField

connect('StockSimulator')

class Stock(EmbeddedDocument):
    name = StringField(required = True)
    symbol = StringField(required = True)
    price = FloatField(required = True)
    delta = FloatField(required = True)


class OwnedStock(EmbeddedDocument):
    name = StringField(required = True)
    stock = EmbeddedDocumentField(Stock, required = True)
    shareCount = FloatField(required = True)
    value = FloatField(required = True)


class User(Document):
    username = StringField(required = True, unique = True)
    email = StringField(required = True, unique = True)
    password = StringField(required = True)
    watchList = SortedListField(EmbeddedDocumentField(Stock), ordering = 'name')
    balence = FloatField(default = 10000.00)
    ownedStock = SortedListField(EmbeddedDocumentField(OwnedStock), ordering = 'name')
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
    user = User(username, email, password)
    # apple = newStock(apple)
    # use the scrape to get info by name
    # then store the info into watchlist
    # defualt watclist: apple, google, amazon.........
    user.save()
    return 'success'

def newStock(name, symbol, price, delta):
    if 

#def updateStockInfo()



