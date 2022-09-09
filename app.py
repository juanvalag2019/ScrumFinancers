from flask import Flask
from flask import render_template
import services.stock_service
import services.crypto_service
from services.user_service import user_service
from services.stock_service import stock_service
from services.crypto_service import crypto_service

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stock", methods=['GET'])
def get_stock_values():
    return stock_service.get_stock_values_from_db()

@app.route("/crypto", methods=['GET'])
def get_crypto_values():
    return crypto_service.get_crypto_values_from_db()

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
