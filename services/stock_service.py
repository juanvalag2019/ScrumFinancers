import datetime
import os
import time
import finnhub
from threading import Thread
from dotenv import load_dotenv
from constants import API_UPDATE_INTERVAL
from models import StockHistory
from models import Stock
from repository.stock_repository import stock_repository
from services.user_service import user_service

class StockService(Thread):

    def __init__(self) :
        Thread.__init__(self)
        load_dotenv()
        self.api_client=finnhub.Client(api_key=os.environ['STOCK_API_KEY'])
        self.stock_names=[{
            'symbol':'AAPL', 'name':'Apple'
        }, {
            'symbol':'GOOGL', 'name':'Google'
        }, {
            'symbol':'AMZN', 'name':'Amazon'
        }]
        self.stocks=[]
        self.updating_stocks=False
        self.update_interval=API_UPDATE_INTERVAL
        self.last_update=None
        self.last_stock_values=None
        self.set_stock_limits()
    
    def start_updating_stocks(self):
        self.updating_stocks=True
        return super().start()
        

    def get_stock_value(self, symbol):
        return self.api_client.quote(symbol)['c']

    def get_user_stocks_values(self):
        stock_updates=[]
        for stock in self.stock_names:
            current_price=self.get_stock_value(stock['symbol'])
            stock_updates.append({
                'name':stock['name'],
                'value':current_price
            })
        return stock_updates

    def run(self):
        while(self.updating_stocks):
            stock_updates=self.get_user_stocks_values()
            if(self.last_update):
                self.last_update=self.last_update+datetime.timedelta(seconds=self.update_interval)
            else:
                self.last_update=datetime.datetime.now()
            updates_to_email=[]
            for stock_update,stock in zip(stock_updates,self.stocks):
                stock_update['timestamp']=self.last_update
                stock_name=stock_update['name']
                current_stock_value=stock_update['value']
                stock_repository.save_stock_update(stock_name, StockHistory(value=current_stock_value, timestamp=stock_update['timestamp']))
                if(self.stock_update_exceed_limit(stock,stock_update)):
                    updates_to_email.append({'name':stock_name, 'value':current_stock_value,'limit':stock['limit'],'is_stock':True })
            if(updates_to_email):
                user_service.send_email_updates(updates_to_email)
            self.last_stock_values=stock_updates
            print(stock_updates)
            time.sleep(self.update_interval)
    
    def stop_updating_stocks(self):
        self.updating_stocks=False
    
    def save_stock_update(self, name, timestamp, value):
        stock_update = StockHistory(timestamp=timestamp,value=value)
        stock_repository.save_stock_update(name,stock_update)

    def create_stock(self,name,limit):
        stock=Stock(name=name, limit=limit)
        return stock_repository.save_stock(stock)

    def set_stock_limits(self):
        for stock_name in self.stock_names:
            stock=stock_repository.get_stock(stock_name['name'])
            if(stock != None):
                stock_name['limit']=stock.limit
                self.stocks.append(stock_name)

    def stock_update_exceed_limit(self, stock, stock_update):
        if(stock['name']==stock_update['name']):
            limit=stock['limit']
            if(stock_update['value']>limit):
                return True
            return False
    

stock_service=StockService()
stock_service.start_updating_stocks()