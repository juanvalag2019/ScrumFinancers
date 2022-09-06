from mongoengine import *
import database

class User(Document):
    email=EmailField(Required=True)
    meta = {
        'collection': 'user'
    }

class StockHistory(EmbeddedDocument):
    value=FloatField(Required=True)
    timestamp=DateTimeField(Required=True)

class Stock(Document):
    name=StringField(Required=True)
    limit=FloatField(Required=True)
    StockHistory=ListField(EmbeddedDocumentField(StockHistory))
    meta = {
        'collection': 'Stock'
    }

class CryptoHistory(EmbeddedDocument):
    value=FloatField(Required=True)
    timestamp=DateTimeField(Required=True)

class Crypto(Document):
    name=StringField(Required=True)
    limit=FloatField(Required=True)
    CryptoHistory=ListField(EmbeddedDocumentField(CryptoHistory))
    meta = {
        'collection': 'Crypto'
    }