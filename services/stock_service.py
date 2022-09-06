import os
import finnhub
from dotenv import load_dotenv

class StockService:

    def __init__(self) :
        load_dotenv()
        self.api_client=finnhub.Client(api_key=os.environ['STOCK_API_KEY'])
        self.stock_names=['AAPL', 'GOOGL', 'AMZN']
        

    def get_stock_value(self, symbol):
        return self.api_client.quote(symbol)['c']

    def get_user_stocks_values(self):
        for stock in self.stock_names:
            current_price=self.get_stock_value(stock)
            print(current_price)

stock_service=StockService()