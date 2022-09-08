from models import Stock
from mongoengine.errors import DoesNotExist, ValidationError,NotUniqueError


class StockRepository:
    def save_stock_update(self, stock_name, stock_update):
        stock=self.get_stock(stock_name)
        if stock != None:
            stock.stock_history.append(stock_update)
            stock.save()
            return True
        return False

    def save_stock(self, stock):
        try:
            stock.validate()
            stock.save()
            return stock
        except (ValidationError,NotUniqueError):
            return None

    def get_stock(self,name):
        try:
            stock=Stock.objects(name=name).get()
            return stock
        except DoesNotExist:
            return None


stock_repository = StockRepository()