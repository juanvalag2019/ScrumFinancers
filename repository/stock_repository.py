from models import Stock


class StockRepository:
    def save_stock(self, stock):
        stock.save()
        return stock


stock_repository = StockRepository()