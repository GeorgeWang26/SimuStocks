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
    balence = FloatField(default = 10000.00)
    ownedStock = SortedListField(EmbeddedDocumentField(OwnedStock), ordering = 'name')
    totalStockValue = FloatField(default = 0.00)
    watchList = SortedListField(EmbeddedDocumentField(Stock), ordering = 'name')
    meta = {
        'ordering': ['+username']
    }


def newUser(username, email, password):
    if User.objects(username = username):





