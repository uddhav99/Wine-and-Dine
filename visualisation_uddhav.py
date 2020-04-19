import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import os

def join(conn, cur):
    cur.execute('''SELECT Popular_Restaurants.restaurant_name, Popular_Restaurants.price, Popular_Restaurants.rating, Popular_Restaurants.review_count,
                 Central_Park_Zomato.price, Central_Park_Zomato.rating, Central_Park_Zomato.review_count FROM Popular_Restaurants JOIN Central_Park_Zomato
                 ON Central_Park_Zomato.restaurant_name = Popular_Restaurants.restaurant_name''')
    data = cur.fetchall()
    column_names = ["restaurant_name", "yelp_price", "yelp_rating", "yelp_reviews", "zomato_price", "zomato_rating", "zomato_reviews"]
    df = pd.DataFrame(data, columns=column_names)

    #dropping shake shack duplicates
    df.drop_duplicates(subset = 'restaurant_name', keep = 'first', inplace=True)
    # converting yelp price from object to float
    df['yelp_price'] = df.yelp_price.astype(float)

    df.sort_values(["yelp_price"], axis=0, inplace= True, ascending = True)
    df['average_price'] = (df['yelp_price'] + df['zomato_price'])/2 #write calculation to file

    # Yelp + Zomato + Average price - line graph 
    fig = go.Figure(data=[go.Scatter(name = "Yelp Price", x = df['restaurant_name'], y = df['yelp_price'], 
                        mode = 'lines+markers'), go.Scatter(name = "Zomato Price", x = df['restaurant_name']
                        , y = df['zomato_price'], mode = 'lines+markers'), go.Scatter(name = "Average Price", 
                        x = df['restaurant_name'], y = df['average_price'], mode = 'lines+markers')])
    
    fig.update_layout(title = 'PRICE COMPARISON', margin = dict(l=50, r=50, b=100, t=100), yaxis_title = "Price Index"
                    , xaxis_title = "Restaurant Name", yaxis = dict(range=[0,5]), width = 750, height = 750, 
                    xaxis_tickangle = -45, xaxis= {'tickmode':'linear'})

    plotly.offline.plot(fig, filename = "./visualisations/price-comaprison.html") #autoopen = False

    df.sort_values('yelp_rating', axis = 0, inplace = True, ascending = True)
    df['average_rating'] = (df['yelp_rating'] + df['zomato_rating']) / 2 #write calculations to file

    # Yelp + Zomato + Average rating - line graph 
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(name = "Yelp Rating", x = df['restaurant_name'], y = df['yelp_rating'], mode = 'lines+markers'))
    fig2.add_trace(go.Scatter(name = "Zomato Rating", x = df['restaurant_name'], y = df['zomato_rating'], mode = 'lines+markers'))
    fig2.add_trace(go.Scatter(name = "Average Rating", x = df['restaurant_name'], y = df['average_rating'], mode = 'lines+markers'))
    fig2.update_layout(title = 'RATING COMPARISON', margin = dict(l=50, r=50, b=100, t=100), yaxis_title = "Rating Index"
                    ,xaxis_title = "Restaurant Name", yaxis = dict(range=[3,5]), width = 750, height = 750, xaxis_tickangle = -45, xaxis= {'tickmode':'linear'})

    plotly.offline.plot(fig2, filename = "./visualisations/rating-comaprison.html") #autoopen = False

    fig3 = go.Figure()

    # does yelp reviews have any correlation with zomato reviews - scatter plots
    fig3.add_trace(go.Scatter(name = "", x = df['zomato_reviews'], y = df['yelp_reviews'], mode = 'markers', text = df['restaurant_name']))
    fig3.update_layout(title_text = 'Zomato vs Yelp (Review Counts)', margin = dict(l=50, r=50, b=100, t=100), yaxis_title = "Yelp reviews",
                        xaxis_title = "Zomato reviews", width = 500, height = 500)
    
    plotly.offline.plot(fig3, filename = "./visualisations/review-correlation.html")

    df.to_csv("Calculations.csv",index=False)

def scatter_plot(conn, cur):
    cur.execute('''SELECT Popular_Restaurants.restaurant_name, Popular_Restaurants.rating, Popular_Restaurants.price, 
                Popular_Restaurants.review_count FROM Popular_Restaurants''')
    data = cur.fetchall()
    column_names = ["restaurant_name", "rating", "price", "reviews"]
    yelp = pd.DataFrame(data, columns=column_names)
    yelp['price'] = yelp.price.astype(float)
    cur.execute('''SELECT Central_Park_Zomato.restaurant_name, Central_Park_Zomato.rating, Central_Park_Zomato.price, 
                Central_Park_Zomato.review_count FROM Central_Park_Zomato''')
    data2 = cur.fetchall()
    zomato = pd.DataFrame(data2, columns=column_names)

    #yelp price vs rating 1,1 
    #zomato price vs rating 1,2

    # Price VS Review Count - is there a correlation between those 
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Yelp", "Zomato"))

    fig.add_trace(go.Scatter(name = "YELP", x = yelp['price'], y = yelp['reviews'], mode = 'markers', text = yelp['restaurant_name']), row = 1, col = 1)
    fig.add_trace(go.Scatter(name = "ZOMATO", x = zomato['price'], y = zomato['reviews'], mode = 'markers', text = zomato['restaurant_name']), row = 1, col = 2)
    fig.update_xaxes(title_text = "Price Index", row=1, col=1)
    fig.update_yaxes(title_text = "Review Count", row=1, col=1)
    fig.update_xaxes(title_text = "Price Index", row=1, col=2)
    fig.update_yaxes(title_text = "Review Count", row=1, col=2)
    fig.update_layout(title_text = 'Price vs Review Count', width = 1000, height = 500, margin = dict(l=50, r=50, b=100, t=100))

    plotly.offline.plot(fig, filename = "./visualisations/price-vs-rating.html") #autoopen = False

def chloropleth_maps(conn, cur):
    token = "pk.eyJ1IjoidWRkaGF2OTkiLCJhIjoiY2s5NXdtcmp4MG5iejNlcnV4MmU0ZmFuZiJ9.745kg7q1OwIntNaN8YAgsQ"
    cur.execute('''SELECT Popular_Restaurants.restaurant_name, Popular_Restaurants.rating, Popular_Restaurants.price, 
                Popular_Restaurants.lat, Popular_Restaurants.long FROM Popular_Restaurants''')
    data = cur.fetchall()
    column_names = ["restaurant_name", "rating", "price", "latitude", "longitude"]
    yelp = pd.DataFrame(data, columns=column_names)
    yelp['price'] = yelp.price.astype(float)
    cur.execute('''SELECT Central_Park_Zomato.restaurant_name, Central_Park_Zomato.rating, Central_Park_Zomato.price, 
                Central_Park_Zomato.lat, Central_Park_Zomato.long FROM Central_Park_Zomato''')
    data2 = cur.fetchall()
    zomato = pd.DataFrame(data2, columns=column_names)

    combined = pd.concat([yelp,zomato])
    combined.drop_duplicates(subset = 'restaurant_name', keep = 'first', inplace=True)

    # scatter map for YELP and Zomato - based on prices
    fig = go.Figure(go.Scattermapbox(lat=combined['latitude'], lon=combined['longitude'], mode = 'markers', marker = {'color':combined['price'],
                'colorscale':'Viridis', 'showscale':True}, hoverinfo = 'lat+lon+text', hovertext = combined['restaurant_name']))
    
    fig.update_layout(title = "Distribution of restaurants, colored by price index", mapbox = dict(accesstoken = token,
                        style = 'dark', zoom = 12.0, center = {'lat': 40.75113, 'lon':-73.97347}))

    plotly.offline.plot(fig, filename = "./visualisations/scattermap-price.html")

    #scatter map of YELP and Zomato - based on ratings
    fig2 = go.Figure(go.Scattermapbox(lat=combined['latitude'], lon=combined['longitude'], mode = 'markers', marker = {'color':combined['rating'],
                'colorscale':'Viridis', 'showscale':True}, hoverinfo = 'lon+lat+text', hovertext = combined['restaurant_name']))
    
    fig2.update_layout(title = "Distribution of restaurants, colored by rating", mapbox = dict(accesstoken = token,
                        style = 'dark', zoom = 12.0, center = {'lat': 40.75113, 'lon':-73.97347}))

    plotly.offline.plot(fig2, filename = "./visualisations/scattermap-ratings.html")


if __name__ == "__main__":
    conn = sqlite3.connect('restaurants.sqlite')
    cur = conn.cursor()
    scatter_plot(conn, cur)
    join(conn, cur)
    chloropleth_maps(conn, cur)
