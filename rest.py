#!/usr/bin/env python

#import necessary libraries
# pip install flask 
#export FLASK_APP=flask-app
#flask run
from flask import Flask, json, render_template, request
import os
import pandas as pd

#create instance of Flask app
app = Flask(__name__)

#decorator 
@app.route("/")
def echo_hello():
    return "<p>Hello World!</p>"



@app.route("/all")
def my_func():
     df = pd.read_csv("./static/restaurant_dataframe.csv")
    #render template is always looking in tempate folder
     return render_template('index.html',  tables=[df.to_html(classes='data', header="true")])



if __name__ == "__main__":
    app.run(debug=True)
