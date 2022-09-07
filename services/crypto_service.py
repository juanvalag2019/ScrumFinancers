import datetime
import os
import time
import finnhub
from threading import Thread
from dotenv import load_dotenv
from constants import API_UPDATE_INTERVAL
from models import Crypto
from repository.crypto_repository import crypto_repository

class CryptoService (Thread):
    def stop_updating_crypto(self):
        self.updating_crypto=False
    
    def crypto_value(self,name,limit):
        crypto=Crypto(name=name, limit=limit)
        return crypto_repository.save_crypto(crypto)

crypto_service=CryptoService()
print(crypto_service.crypto_value('Juan',5.3).id)