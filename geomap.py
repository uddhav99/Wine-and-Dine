import plotly.express as px
import pandas as pd
import sqlite3
px.set_mapbox_access_token('pk.eyJ1IjoiYW1hemlubWV0czY5ODYiLCJhIjoiY2szYWxxN2g0MDNsMTNrbnZ3ZTA2ZDRxMSJ9.Pfh92OzLf2Gp91Sgt6foAw')
conn = sqlite3.connect('restaurants.sqlite')
cur = conn.cursor()
cur.execute('SELECT * from Popular_Restaurants')
restaurant_data = cur.fetchall()
# fig = px.bar(newdata,x='category',y='count',color='location',barmode='group',title='Number of Restaurants by Category near Central Park, Times Square, or the World Trade Center from Yelp Search')
# fig = px.scatter_mapbox(df4, lat="lat", lon="long", color="review_count", text = "category", hover_name = "restaurant_name", size="rating",
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
# fig.show()