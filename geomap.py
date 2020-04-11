import plotly.express as px
import pandas as pd
px.set_mapbox_access_token('pk.eyJ1IjoiYW1hemlubWV0czY5ODYiLCJhIjoiY2szYWxxN2g0MDNsMTNrbnZ3ZTA2ZDRxMSJ9.Pfh92OzLf2Gp91Sgt6foAw')
df = pd.read_csv('Central_Park.csv')
# fig = px.scatter_mapbox(df, lat="lat", lon="long", color="review_count", text = "category", hover_name = "restaurant_name", size="rating",
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
df2 = pd.read_csv('Times_Square.csv')
df3 = pd.read_csv('World_Trade_Center.csv')
df4 = pd.concat([df,df2,df3],ignore_index=True)
# print(df4)
location_list = []
for i in range(200):
    location_list.append("Central Park")
for i in range(200,402):
    location_list.append("Times Square")
for i in range(402,602):
    location_list.append("World Trade Center")
print(len(location_list))
df4.insert(1,"location",location_list)
# print(df4)
newdata = df4.groupby(['category','location'])["location"].count().reset_index(name ="count")
print(newdata)
# fig = px.bar(newdata,x='category',y='count',color='location',barmode='group',title='Number of Restaurants by Category near Central Park, Times Square, or the World Trade Center from Yelp Search')
fig = px.scatter_mapbox(df4, lat="lat", lon="long", color="review_count", text = "category", hover_name = "restaurant_name", size="rating",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
fig.show()