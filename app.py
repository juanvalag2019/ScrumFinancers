from flask import Flask, request
from flask import render_template
import services.stock_service
import services.crypto_service
from services.user_service import user_service

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/useremail", methods=['POST'])
def subscribe_email():
    if(request.method=="POST"):
        user_service.create_user(request.form['useremail'])
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='127.0.0.1')
