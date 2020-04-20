import requests
import json
import sqlite3
import time
import pandas as pd

def setUpDatabase(data,conn,cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS Popular_Restaurants (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, address TEXT, lat REAL, long REAL, rating REAL, price TEXT,category_id INTEGER,review_count INTEGER)''')
    for business in data["businesses"]:
        restaurant_id = business['id']
        name = business['name']
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
        cur.execute('SELECT id FROM Categories_Yelp WHERE title= ?',(business['categories'][0]['title'],))
        category_id = cur.fetchone()[0]
        review_count = business['review_count']
        cur.execute("INSERT OR IGNORE INTO Popular_Restaurants (restaurant_id,restaurant_name,address,lat,long,rating,price,category_id,review_count) VALUES (?,?,?,?,?,?,?,?,?)",(restaurant_id,name,address,lat,longitude,rating,price,category_id,review_count))
        conn.commit()

def getCategories(data,conn,cur):
    category_list = []
    for business in data['businesses']:
        business_categories = business['categories']
        for category in business_categories:
            if category['title'] not in category_list:
                category_list.append(category['title'])

    cur.execute("CREATE TABLE IF NOT EXISTS Categories_Yelp (id INTEGER PRIMARY KEY, title TEXT UNIQUE)")
    for i in range(len(category_list)):
        cur.execute("INSERT OR IGNORE INTO Categories_Yelp (title) VALUES (?)",(category_list[i], ))
    conn.commit()
    
def getData(location,offset):
    conn = sqlite3.connect('restaurants.sqlite')
    cur = conn.cursor()
    api_key = 'ViVcJp0uJf0RJ32VQJKZIDhWxRfSS08elfK4fX31-s8BuL2nUT8h-b50QsPDHbWDOmt3NqAPu8e0rjPhVoupai8KwCGLa6EZmR4nZARu3P2g6k_JpT9-CxQXfguNXnYx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url='https://api.yelp.com/v3/businesses/search'
    params = {'location':location,'categories':'restaurants','offset':offset}
    try:
        req=requests.get(url, params=params, headers=headers)
        print("Fetching data from Yelp API...")
        data = json.loads(req.text)
        getCategories(data,conn,cur)
        setUpDatabase(data,conn,cur)
    except:
        print("Exception")
        data = {}
    print('Pausing for a bit...')
    time.sleep(5)
if __name__ == "__main__":
    offset = input("Enter an offset: ")
    getData('NYC',offset)
    # getCategories()