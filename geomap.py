import plotly.express as px
import pandas as pd
px.set_mapbox_access_token('pk.eyJ1IjoiYW1hemlubWV0czY5ODYiLCJhIjoiY2szYWxxN2g0MDNsMTNrbnZ3ZTA2ZDRxMSJ9.Pfh92OzLf2Gp91Sgt6foAw')
df = pd.read_csv('Central_Park.csv')
# fig = px.scatter_mapbox(df, lat="lat", lon="long", color="review_count", text = "category", hover_name = "restaurant_name", size="rating",
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

# fig = px.bar(df,x='category',y='review_count',color='rating',barmode='group',hover_name='restaurant_name')
# fig.show()