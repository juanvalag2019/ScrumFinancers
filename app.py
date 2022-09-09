from flask import Flask
from flask import render_template, jsonify
from services.stock_service import stock_service
from services.crypto_service import crypto_service

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stocks", methods=['GET'])
def get_stock_values():
    return jsonify(stock_service.get_stocks_history())

@app.route("/cryptos", methods=['GET'])
def get_crypto_values():
    return jsonify(crypto_service.get_cryptos_history())

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
