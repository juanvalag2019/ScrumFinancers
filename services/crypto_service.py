import datetime
import os
import time
import finnhub
from threading import Thread
from dotenv import load_dotenv
from constants import API_UPDATE_INTERVAL
from models import Crypto
from models import CryptoHistory
from repository.crypto_repository import crypto_repository

class CryptoService (Thread):
    def stop_updating_crypto(self):
        self.updating_crypto=False

    def save_crypto_update(self, name, timestamp, value):
        crypto_update = CryptoHistory(timestamp=timestamp,value=value)
        crypto_repository.save_crypto_update(name,crypto_update)

    def create_crypto(self,name,limit):
        crypto=Crypto(name=name, limit=limit)
        return crypto_repository.save_crypto(crypto)

crypto_service=CryptoService()




