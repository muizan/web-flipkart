
from email import header
from email.quoprimime import body_check
from itertools import product
from math import prod
from bs4 import BeautifulSoup
import requests
import smtplib
import time
import os
from flask import Flask, appcontext_popped,redirect,url_for,render_template,request,send_from_directory


# URL =  'https://www.flipkart.com/adidas-accelar-m-running-shoes-men/p/itm2b3cbf3dbd64c?pid=SHOG9XNXZHHKFQZ7&lid=LSTSHOG9XNXZHHKFQZ7DA1OPL&marketplace=FLIPKART&q=adidas+shoes&store=osp%2Fcil%2F1cu&srno=s_1_9&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&fm=search-autosuggest&iid=00732304-985e-425d-b70a-a8ced7155762.SHOG9XNXZHHKFQZ7.SEARCH&ppt=sp&ppn=sp&ssid=bkvbno0y000000001655753373337&qH=09d26a302946ebcb'
# product=URL;
headers ={"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'}
app = Flask(__name__)
    

def check_price(data):
    while(1):
      page =requests.get(data[1],headers=headers)
      soup=BeautifulSoup(page.content,'html.parser')
      details =soup.find("h1",{"class":"yhB1nd"}).get_text();
      price =soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text();
      convertedPrice=0
      for i in range (1,len(price)):
        if(price[i]!=','):
          convertedPrice=convertedPrice*10 + (ord(price[i])-48)
      rice=0
      for i in range (0,len(data[2])):
        rice=rice*10 + (ord(data[2][i])-48) 
      print(convertedPrice)
      print(details)
      if(convertedPrice>rice):
         send_mail(data[0],data[1])
      

def send_mail(data,URL):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('abhisheksha952@gmail.com','konrvplwrxrlpynv')
    subject ='price fell down!'
    body = 'check the flipkart link '+ URL
    msg =f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'abhisheksha952@gmail.com',
        data,
         msg
     )
    print('hey email has been sent!')
    server.quit()


def index():
    return render_template('base.html')
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        customerPrice = request.form["num"]
        customerAddress= request.form["nm"]
        produc = request.form["prod"]
        data=[customerAddress,produc,customerPrice]
        check_price(data)
        return redirect(url_for("user",usr=customerPrice))
    else:
        return render_template("base.html")
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
         'favicon.ico',mimetype='image/vnd.microsoft.icon')      
@app.route("/<usr>")
def user(usr):
    return render_template("base.html");

if __name__ == "__main__":
    app.run(debug=True)
