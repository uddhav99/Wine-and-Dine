import requests
import json
import sqlite3
import time

def setUpDatabase(data):
    conn = sqlite3.connect('yelp.sqlite')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Restaurants (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, address TEXT, lat REAL, long REAL, rating REAL, price TEXT,category TEXT,review_count INTEGER)''')
    restaurant_list = []
    for business in data["businesses"]:
       restaurant_id = business['id']
       name = business['name']
       address = business['location']['address1']
       lat = business['coordinates']['latitude']
       longitude = business['coordinates']['longitude']
       rating = business['rating']
       if 'price' in business:
           price = business['price']
       else:
           price = '$$$$'
       category = business['categories'][0]['title']
       review_count = business['review_count']
       business_tuple = (restaurant_id,name,address,lat,longitude,rating,price,category,review_count)
       restaurant_list.append(business_tuple)
    for i in range(len(restaurant_list)):
        cur.execute("INSERT OR IGNORE INTO Restaurants (restaurant_id,restaurant_name,address,lat,long,rating,price,category,review_count) VALUES (?,?,?,?,?,?,?,?,?)",(restaurant_list[i][0],restaurant_list[i][1],restaurant_list[i][2],restaurant_list[i][3],restaurant_list[i][4],restaurant_list[i][5],restaurant_list[i][6],restaurant_list[i][7],restaurant_list[i][8]))
    conn.commit()

def getData():
    api_key = 'ViVcJp0uJf0RJ32VQJKZIDhWxRfSS08elfK4fX31-s8BuL2nUT8h-b50QsPDHbWDOmt3NqAPu8e0rjPhVoupai8KwCGLa6EZmR4nZARu3P2g6k_JpT9-CxQXfguNXnYx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url='https://api.yelp.com/v3/businesses/search'
    value = str(input("Please enter a Yelp category: "))
    params = {'latitude':'40.7465','longitude':'-74.0014','radius':'8047','categories':value}
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
getData()