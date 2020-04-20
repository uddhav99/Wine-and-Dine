import requests
import json
import sqlite3
import time
import pandas as pd
import re

def set_table(data, conn, cur):

    cur.execute('''CREATE TABLE IF NOT EXISTS Zomato_Restaurants (restaurant_id TEXT PRIMARY KEY, restaurant_name TEXT, address TEXT, lat REAL, long REAL, rating REAL, price REAL,category INTEGER,review_count INTEGER)''')

    for restaurant in data["restaurants"]:
        restaurant_id = restaurant["restaurant"]["id"]
        name = restaurant["restaurant"]["name"]
        address = restaurant["restaurant"]["location"]["address"]
        latitude = float(restaurant["restaurant"]["location"]["latitude"])
        longitude = float(restaurant["restaurant"]["location"]["longitude"])
        rating = float(restaurant["restaurant"]["user_rating"]["aggregate_rating"])
        price = restaurant["restaurant"]["price_range"]
        cuisine = restaurant["restaurant"]["cuisines"]
        category = cuisine.split(',')[0]
        cur.execute('SELECT id FROM Categories_Zomato WHERE title= ?',(category,))
        category_id = cur.fetchone()[0]
        review_count = restaurant["restaurant"]["all_reviews_count"]
        cur.execute("INSERT OR IGNORE INTO Zomato_Restaurants (restaurant_id,restaurant_name,address, lat, long, rating, price, category, review_count) VALUES (?,?,?,?,?,?,?,?,?)", (restaurant_id, name, address, latitude, longitude, rating, price, category_id, review_count))

        conn.commit()


def getCategories(data,conn,cur):
    category_list = []
    for restaurant in data['restaurants']:
        cuisines = restaurant["restaurant"]["cuisines"]
        category = cuisines.split(',')
        for cuisine in category:
            if cuisine.strip() not in category_list:
                category_list.append(cuisine.strip())

    cur.execute("CREATE TABLE IF NOT EXISTS Categories_Zomato (id INTEGER PRIMARY KEY, title TEXT UNIQUE)")
    for i in range(len(category_list)):
        cur.execute("INSERT OR IGNORE INTO Categories_Zomato (title) VALUES (?)",(category_list[i], ))
    conn.commit()

def get_data(latitude, longitude, offset):
    conn = sqlite3.connect('restaurants.sqlite')
    cur = conn.cursor()
    api_key = "acbe0ae5e8a689201ddcedb43ad95579"
    base_url = "https://developers.zomato.com/api/v2.1/search?"
    headers = {'Accept':'application/json', 'user-key': api_key}
    params = {'start':offset, 'count':20, 'lat':latitude, 'lon':longitude, 'radius':805} 
    #try:
    #check = base_url + "start=" + str(offset) + "&lat=" + str(latitude) + "&lon=" + str(longitude) + "&radius=805"  
    req=requests.get(base_url, params = params, headers=headers)
    print("Fetching data from Zomato API...")
    data = json.loads(req.text)
    getCategories(data, conn, cur)
    set_table(data,conn, cur)
    #except:
     #   print("Exception")
      #  data ={}
    print("Pausing for a bit...")
    time.sleep(5)


if __name__ == "__main__":
    offset = input("Enter an offset: ")
    # get_data(40.7127,-74.0134,offset,'Times Square')
    get_data('40.7127','-74.0134',offset)