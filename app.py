from firebase import firebase
from email import header
from email.quoprimime import body_check
from math import prod
from bs4 import BeautifulSoup
import requests
import smtplib
import time
import os
from flask import Flask, appcontext_popped,redirect,url_for,render_template,request,send_from_directory

#headers is used to identify the version of browser i am using
headers ={"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'}
app = Flask(__name__)


#FBconn is used to establish a connection between firebase and my program 
FBconn=firebase.FirebaseApplication('https://my-web-scrapper-3dff1-default-rtdb.firebaseio.com/',None)
#def of the flask app


def index():
    return render_template('base.html')


@app.route("/", methods=["POST", "GET"])


def login():
    if request.method == "POST":
        customerPrice = request.form["num"]
        customerAddress= request.form["nm"]
        produc = request.form["prod"]
        data_to_upload={
            'customerEmaiil':customerAddress,
            'desiredPrice':customerPrice,
            'product' :produc        
        }
        result = FBconn.post('/customerList/',data_to_upload)
        return redirect(url_for("user",usr=customerPrice))
    else:
        return render_template("base.html")
@app.route('/favicon.ico')

def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico',mimetype='image/vnd.microsoft.icon') 

@app.route("/<usr>")

def user(usr):
    return render_template("notified.html")
if __name__ == "__main__":
    app.run(debug=True)
