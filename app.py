from flask import Flask
from flask import render_template
import services.stock_service
import services.crypto_service

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
