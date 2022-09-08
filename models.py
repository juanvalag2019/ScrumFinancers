from mongoengine import *
import database

class User(Document):
    email=EmailField(required=True,unique=True)
    meta = {
        'collection': 'user'
    }

class StockHistory(EmbeddedDocument):
    value=FloatField(required=True)
    timestamp=DateTimeField(required=True)

class Stock(Document):
    name=StringField(required=True,unique=True)
    limit=FloatField(required=True)
    stock_history=ListField(EmbeddedDocumentField(StockHistory))
    meta = {
        'collection': 'Stock'
    }

class CryptoHistory(EmbeddedDocument):
    value=FloatField(required=True)
    timestamp=DateTimeField(required=True)

class Crypto(Document):
    name=StringField(required=True,unique=True)
    limit=FloatField(required=True)
    crypto_history=ListField(EmbeddedDocumentField(CryptoHistory))
    meta = {
        'collection': 'Crypto'
    }