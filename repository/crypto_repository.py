from models import Crypto
from mongoengine.errors import DoesNotExist, ValidationError,NotUniqueError 

class CryptoRepository:
    def save_crypto_update(self, crypto_name, crypto_update):
        crypto=self.get_crypto(crypto_name)
        if crypto != None:
            crypto.crypto_history.append(crypto_update)
            crypto.save()
            return True
        return False

    def save_crypto(self, crypto):
        try:
            crypto.validate()
            crypto.save()
            return crypto
        except (ValidationError,NotUniqueError):
            return None

    def get_crypto(self,name):
        try:
            crypto=Crypto.objects(name=name).get()
            return crypto
        except DoesNotExist:
            return None

crypto_repository = CryptoRepository()
