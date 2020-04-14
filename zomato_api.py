import requests
import json
import sqlite3
import time
import pandas as pd
import re

def set_table(data, location):
    conn = sqlite3.connect('restaurants.sqlite')
    cur = conn.cursor()

    if location == "Times Square":
        cur.execute('''CREATE TABLE IF NOT EXISTS Times_Square_Zomato (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, address TEXT, lat REAL, long REAL, rating REAL, price REAL,category TEXT,review_count INTEGER)''')
        table = "Times_Square_Zomato"
    elif location == "Central Park":
        cur.execute('''CREATE TABLE IF NOT EXISTS Central_Park_Zomato (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, address TEXT, lat REAL, long REAL, rating REAL, price REAL,category TEXT,review_count INTEGER)''')
        table = "Central_Park_Zomato"
    else:
        cur.execute('''CREATE TABLE IF NOT EXISTS World_Trade_Center_Zomato (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, address TEXT, lat REAL, long REAL, rating REAL, price REAL,category TEXT,review_count INTEGER)''')
        table = "World_Trade_Center_Zomato"

    category_list = []

    for restaurant in data["restaurants"]:
        restaurant_id = restaurant["restaurant"]["id"]
        name = restaurant["restaurant"]["name"]
        address = restaurant["restaurant"]["location"]["address"]
        latitude = float(restaurant["restaurant"]["location"]["latitude"])
        longitude = float(restaurant["restaurant"]["location"]["longitude"])
        rating = float(restaurant["restaurant"]["user_rating"]["aggregate_rating"])
        price = restaurant["restaurant"]["price_range"]
        cuisine = restaurant["restaurant"]["cuisines"]
        first_cuisine = re.search(r'^\w*\b', cuisine)
        category = first_cuisine[0]
        review_count = restaurant["restaurant"]["all_reviews_count"]
        if location == "Times Square":
            cur.execute("INSERT OR IGNORE INTO Times_Square_Zomato (restaurant_id,restaurant_name,address, lat, long, rating, price, category, review_count) VALUES (?,?,?,?,?,?,?,?,?)", (restaurant_id, name, address, latitude, longitude, rating, price, category, review_count))
        elif location == "Central Park":
            cur.execute("INSERT OR IGNORE INTO Central_Park_Zomato (restaurant_id,restaurant_name,address, lat, long, rating, price, category, review_count) VALUES (?,?,?,?,?,?,?,?,?)", (restaurant_id, name, address, latitude, longitude, rating, price, category, review_count))
        else:
            cur.execute("INSERT OR IGNORE INTO World_Trade_Center_Zomato (restaurant_id,restaurant_name,address, lat, long, rating, price, category, review_count) VALUES (?,?,?,?,?,?,?,?,?)", (restaurant_id, name, address, latitude, longitude, rating, price, category, review_count))
        conn.commit()

        if category not in category_list:
            category_list.append(category)

    cur.execute("CREATE TABLE IF NOT EXISTS Categories_Zomato (cuisine TEXT PRIMARY KEY)")
    for c in category_list:
        cur.execute("INSERT OR IGNORE INTO Categories_Zomato (cuisine) VALUES (?)", (c, ))

    conn.commit()



def get_data(latitude, longitude, offset, location):
    api_key = "acbe0ae5e8a689201ddcedb43ad95579"
    base_url = "https://developers.zomato.com/api/v2.1/search?"
    headers = {'Accept':'application/json', 'user-key': api_key}
    params = {'start':offset, 'count':20, 'lat':latitude, 'lon':longitude, 'radius':805} 
    #try:
    #check = base_url + "start=" + str(offset) + "&lat=" + str(latitude) + "&lon=" + str(longitude) + "&radius=805"  
    req=requests.get(base_url, params = params, headers=headers)
    print("Fetching data from Zomato API...")
    data = json.loads(req.text)
    set_table(data,location)
    #except:
     #   print("Exception")
      #  data ={}
    print("Pausing for a bit...")
    time.sleep(5)


if __name__ == "__main__":
    offset = input("Enter an offset: ")
    # get_data(40.7127,-74.0134,offset,'Times Square')
    get_data('40.7127','-74.0134',offset,'Central Park')