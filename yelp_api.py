import requests
import json
import sqlite3
import time
import pandas as pd

def setUpDatabase(data,location):
    conn = sqlite3.connect('restaurants.sqlite')
    cur = conn.cursor()
    if location == "Central Park":
        cur.execute('''CREATE TABLE IF NOT EXISTS Central_Park (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, address TEXT, lat REAL, long REAL, rating REAL, price TEXT,category TEXT,review_count INTEGER)''')
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
                cur.execute("INSERT OR IGNORE INTO Central_Park (restaurant_id,restaurant_name,address,lat,long,rating,price,category,review_count) VALUES (?,?,?,?,?,?,?,?,?)",(restaurant_list[i][0],restaurant_list[i][1],restaurant_list[i][2],restaurant_list[i][3],restaurant_list[i][4],restaurant_list[i][5],restaurant_list[i][6],restaurant_list[i][7],restaurant_list[i][8]))
        conn.commit()
    elif location == "Times Square":
        cur.execute('''CREATE TABLE IF NOT EXISTS Times_Square (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, address TEXT, lat REAL, long REAL, rating REAL, price TEXT,category TEXT,review_count INTEGER)''')
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
                cur.execute("INSERT OR IGNORE INTO Times_Square (restaurant_id,restaurant_name,address,lat,long,rating,price,category,review_count) VALUES (?,?,?,?,?,?,?,?,?)",(restaurant_list[i][0],restaurant_list[i][1],restaurant_list[i][2],restaurant_list[i][3],restaurant_list[i][4],restaurant_list[i][5],restaurant_list[i][6],restaurant_list[i][7],restaurant_list[i][8]))
        conn.commit()
    else:
        cur.execute('''CREATE TABLE IF NOT EXISTS World_Trade_Center (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, address TEXT, lat REAL, long REAL, rating REAL, price TEXT,category TEXT,review_count INTEGER)''')
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
            cur.execute("INSERT OR IGNORE INTO World_Trade_Center (restaurant_id,restaurant_name,address,lat,long,rating,price,category,review_count) VALUES (?,?,?,?,?,?,?,?,?)",(restaurant_list[i][0],restaurant_list[i][1],restaurant_list[i][2],restaurant_list[i][3],restaurant_list[i][4],restaurant_list[i][5],restaurant_list[i][6],restaurant_list[i][7],restaurant_list[i][8]))
        conn.commit()
    
def getData(lat,long_,location,offset):
    api_key = 'ViVcJp0uJf0RJ32VQJKZIDhWxRfSS08elfK4fX31-s8BuL2nUT8h-b50QsPDHbWDOmt3NqAPu8e0rjPhVoupai8KwCGLa6EZmR4nZARu3P2g6k_JpT9-CxQXfguNXnYx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url='https://api.yelp.com/v3/businesses/search'
    params = {'latitude':lat,'longitude':long_,'radius':'1610','categories':'restaurants','offset':offset}
    try:
        req=requests.get(url, params=params, headers=headers)
        print("Fetching data from Yelp API...")
        data = json.loads(req.text)
        setUpDatabase(data,location)
    except:
        print("Exception")
        data = {}
    print('Pausing for a bit...')
    time.sleep(5)
# getData('40.7829','-73.9654','Central Park')
# getData('40.7580','-73.9855','Times Square')
for i in range(1,11):
    offset = 20*i
    getData('40.7580','-73.9855','Times Square',offset)