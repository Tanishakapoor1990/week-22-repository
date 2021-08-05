#!/usr/bin/env python

#import necessary libraries
# pip install flask 
#export FLASK_APP=flask-app
#flask run
from flask import Flask, json, render_template
import requests
import os
import time
from bs4 import BeautifulSoup
import pandas as pd

#create instance of Flask app
app = Flask(__name__)

#decorator 
@app.route("/")
def echo_hello():
    return "<p>Hello World!</p>"

results=[]
def getrestaurants(page):
         #Constructing url 
        url = f'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Maryland%20Heights%2C%20MO&ns=1&start='+str(page)
        #get page with requests
        r = requests.get(url)
           
      # Wait a second  to not over exceed rate
        time.sleep(1.01)
        #Using beautiful soup to parse html data:
        soup = BeautifulSoup(r.text, 'html.parser')
        ## Getting all class names under the below mentioned  class using find_all 
        mains = soup.find_all('div', {'class':"container__09f24__sxa9- hoverable__09f24__3HkY2 margin-t3__09f24__hHZsm margin-b3__09f24__3h89A padding-t3__09f24__1VTAn padding-r3__09f24__11Xv2 padding-b3__09f24__2I83c padding-l3__09f24__1JEx9 border--top__09f24__37VAs border--right__09f24__Z9jGU border--bottom__09f24__3lElq border--left__09f24__akfOa border-color--default__09f24__3Epto"})
#Looping through all mains to get the elements of all tags:
        for main in mains:
            try:            
                name = main.find("a",class_="css-166la90").text
                print("Restaurant name:",name)
                rating = main.find("span",{"class":"display--inline__09f24__nqZ_W border-color--default__09f24__3Epto"}).div.get('aria-label')
                print("Restaurant rating:",rating)
                reviewcount = main.find("span", {"class": "reviewCount__09f24__3GsGY css-e81eai"}).text
                print("Restaurant reviewcount:",reviewcount)
                comment = main.find("p", {"class": "css-e81eai"}).text
                print("Restaurant comment:",comment,'\n')
 #Creating a dictionary           
                rest_dict = {'Name':name,
                           'Rating':rating,
                           'Reviews':reviewcount,
                           'Comments':comment}
                results.append(rest_dict)   #appending the dictionary elements to results list
            except AttributeError as e:
                print(e)
        return results
#Using a for loop to print first 50 restaurants data where 0 is starting page.We are using a for loop
#till 60 as some restaurants were missing the data so we had to do exceptional handling for it.


@app.route("/scrape_rest")
def my_fun():
    for x in range(0,60,10):
        getrestaurants(x)
#Creating dataframe    
    df = pd.DataFrame(results)
    df.to_csv('rest.csv')
    return "<p>Result of 50 restaurants</p>"

@app.route("/all")
def my_func():
     df = pd.read_csv("rest.csv")
    #render template is always looking in tempate folder
     return render_template('index.html',  tables=[df.to_html(classes='data', header="true")])


if __name__ == "__main__":
    app.run(debug=True)
