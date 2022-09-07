import datetime
import os
import time
import finnhub
from threading import Thread
from dotenv import load_dotenv
from constants import API_UPDATE_INTERVAL
from models import Stock
from repository.stock_repository import stock_repository

class StockService(Thread):

    def __init__(self) :
        Thread.__init__(self)
        load_dotenv()
        self.api_client=finnhub.Client(api_key=os.environ['STOCK_API_KEY'])
        self.stock_names=['AAPL', 'GOOGL', 'AMZN']
        self.updating_stocks=False
        self.update_interval=API_UPDATE_INTERVAL
        self.last_update=None
        self.last_stock_values=None
    
    def start_updating_stocks(self):
        self.updating_stocks=True
        return super().start()
        

    def get_stock_value(self, symbol):
        return self.api_client.quote(symbol)['c']

    def get_user_stocks_values(self):
        stock_updates=[]
        for stock in self.stock_names:
            current_price=self.get_stock_value(stock)
            stock_updates.append({
                'name':stock,
                'price':current_price
            })
        return stock_updates

    def run(self):
        while(self.updating_stocks):
            stock_updates=self.get_user_stocks_values()
            if(self.last_update):
                self.last_update=self.last_update+datetime.timedelta(seconds=self.update_interval)
            else:
                self.last_update=datetime.datetime.utcnow()
            for stock_update in stock_updates:
                stock_update['timestamp']=self.last_update
            self.last_stock_values=stock_updates
            print(stock_updates)
            time.sleep(self.update_interval)
    
    def stop_updating_stocks(self):
        self.updating_stocks=False
    
    def stock_value(self,name,limit):
        stock=Stock(name=name, limit=limit)
        return stock_repository.save_stock(stock)
    
            



stock_service=StockService()
print(stock_service.stock_value('Juan',5.3).id)
