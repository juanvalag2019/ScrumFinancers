import datetime
import os
import json
import time
import finnhub
from threading import Thread
from dotenv import load_dotenv
from constants import API_UPDATE_INTERVAL
from models import Crypto
from models import CryptoHistory
from repository.crypto_repository import crypto_repository
from services.user_service import user_service
from requests import Request, Session

class CryptoService(Thread):

    def __init__(self) :
        Thread.__init__(self)
        load_dotenv()
        self.cryptos=[{
            'name': 'Bitcoin'
        },{
            'name': 'Ethereum'
        },{
            'name': 'Maker'
        },]
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        self.parameters = { 'slug': 'bitcoin,ethereum,maker', 'convert': 'USD' }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': os.environ['CRYPTO_API_KEY']
        }
        self.session = Session()
        self.session.headers.update(self.headers)
        self.updating_cryptos=False
        self.update_interval=API_UPDATE_INTERVAL
        self.last_update=None
        self.last_crypto_values=None
        self.set_cryptos_limits()

    def start_updating_cryptos(self):
        self.updating_cryptos=True
        return super().start()

    def get_user_crypto_values(self):
        crypto_updates=[]
        response = self.session.get(self.url, params=self.parameters)
        data= json.loads(response.text)
        for crypto in data['data']:
            crypto_name= data['data'][crypto]['name']
            current_price= data['data'][crypto]['quote']['USD']['price']
            crypto_updates.append({
                'name':crypto_name,
                'value':current_price
            })
        return crypto_updates

    def run(self):
        while(self.updating_cryptos):
            crypto_updates=self.get_user_crypto_values()
            if(self.last_update):
                self.last_update=self.last_update+datetime.timedelta(seconds=self.update_interval)
            else:
                self.last_update=datetime.datetime.now()
            updates_to_email=[]
            for crypto_update, crypto in zip(crypto_updates, self.cryptos):
                crypto_update['timestamp']=self.last_update
                name=crypto_update['name']
                current_value=crypto_update['value']
                crypto_repository.save_crypto_update(name, CryptoHistory(value=current_value, timestamp=crypto_update['timestamp']))
                if(self.crypto_update_exceed_limit(crypto, crypto_update)):
                    updates_to_email.append({'name':name, 'value':current_value,'limit':crypto['limit'],'is_stock':False })
            if(updates_to_email):
                user_service.send_email_updates(updates_to_email)
            self.last_crypto_values=crypto_updates
            print(crypto_updates)
            time.sleep(self.update_interval)
    
    def stop_updating_cryptos(self):
        self.updating_cryptos=False

    def save_crypto_update(self, name, timestamp, value):
        crypto_update = CryptoHistory(timestamp=timestamp,value=value)
        crypto_repository.save_crypto_update(name,crypto_update)

    def create_crypto(self,name,limit):
        crypto=Crypto(name=name, limit=limit)
        return crypto_repository.save_crypto(crypto)

    def set_cryptos_limits(self):
        for crypto in self.cryptos:
            crypto_entity=crypto_repository.get_crypto(crypto['name'])
            crypto['limit']=crypto_entity['limit']

    def crypto_update_exceed_limit(self, crypto, crypto_update):
        if(crypto['name']==crypto_update['name']):
            limit=crypto['limit']
            if(crypto_update['value']>limit):
                return True
            return False

    def get_crypto_values_from_db(self):
        #for crypto_name in self.cryptos:
        #    crypto_repository.get_crypto(stock_name['name'])
        #return
        pass 
            
crypto_service=CryptoService()
crypto_service.start_updating_cryptos()
