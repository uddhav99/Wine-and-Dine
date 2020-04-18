import requests
import json
import sqlite3
import time
import pandas as pd

def setUpDatabase(data):
    conn = sqlite3.connect('restaurants.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Popular_Restaurants (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, location TEXT, address TEXT, lat REAL, long REAL, rating REAL, price TEXT,category TEXT,review_count INTEGER)''')
    for business in data["businesses"]:
        restaurant_id = business['id']
        name = business['name']
        location = business['location']['city']
        address = business['location']['address1']
        lat = business['coordinates']['latitude']
        longitude = business['coordinates']['longitude']
        rating = business['rating']
        if 'price' in business:
            if business['price'] == "$":
                price = 1.0
            elif business['price'] == "$$":
                price = 2.0
            elif business['price'] == "$$$":
                price = 3.0
            else:
                price = 4.0
        else:
            price = 4.0
        category = business['categories'][0]['title']
        review_count = business['review_count']
        cur.execute("INSERT OR IGNORE INTO Popular_Restaurants (restaurant_id,restaurant_name,location,address,lat,long,rating,price,category,review_count) VALUES (?,?,?,?,?,?,?,?,?,?)",(restaurant_id,name,location,address,lat,longitude,rating,price,category,review_count))
        conn.commit()

def getCategories():
    conn = sqlite3.connect('restaurants.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT category FROM Restaurants')
    database_list = cur.fetchall()
    category_list = []
    for item in database_list:
        category_list.append(item[0])
    print(category_list)
    
def getData(location,offset):
    api_key = 'ViVcJp0uJf0RJ32VQJKZIDhWxRfSS08elfK4fX31-s8BuL2nUT8h-b50QsPDHbWDOmt3NqAPu8e0rjPhVoupai8KwCGLa6EZmR4nZARu3P2g6k_JpT9-CxQXfguNXnYx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url='https://api.yelp.com/v3/businesses/search'
    params = {'location':location,'categories':'restaurants','offset':offset}
    try:
        req=requests.get(url, params=params, headers=headers)
        print("Fetching data from Yelp API...")
        data = json.loads(req.text)
        setUpDatabase(data)
    except:
        print("Exception")
        data = {}
    print('Pausing for a bit...')
    time.sleep(5)
# getData('40.7829','-73.9654','Central Park')
# getData('40.7580','-73.9855','Times Square')
if __name__ == "__main__":
    offset = input("Enter an offset: ")
    getData('NYC',offset)
    #getCategories()