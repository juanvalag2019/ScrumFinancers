from models import Crypto

class CryptoRepository:
    def save_crypto(self, crypto):
        crypto.save()
        return crypto

crypto_repository = CryptoRepository()