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

    def serialize(self):
        return {
            'value': self.value,
            'timestamp': self.timestamp
        }

class Stock(Document):
    name=StringField(required=True,unique=True)
    limit=FloatField(required=True)
    stock_history=ListField(EmbeddedDocumentField(StockHistory))
    meta = {
        'collection': 'Stock'
    }

    def serialize(self):
        return {
            'name': self.name,
            'limit': self.limit,
            'history': [update.serialize() for update in self.stock_history]
        }

class CryptoHistory(EmbeddedDocument):
    value=FloatField(required=True)
    timestamp=DateTimeField(required=True)

    def serialize(self):
        return {
            'value': self.value,
            'timestamp': self.timestamp
        }

class Crypto(Document):
    name=StringField(required=True,unique=True)
    limit=FloatField(required=True)
    crypto_history=ListField(EmbeddedDocumentField(CryptoHistory))
    meta = {
        'collection': 'Crypto'
    }

    def serialize(self):
        return {
            'name': self.name,
            'limit': self.limit,
            'history': [update.serialize() for update in self.crypto_history]
        }