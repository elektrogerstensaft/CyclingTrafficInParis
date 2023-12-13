import pandas as pd
import geopandas as gpd
import plotly.express as px

"""
The columns in this file are:
Counter ID
Counting site installation date
Counter name
Counting site ID
Counting site name
Hourly count
Date and time of count
Geographic coordinates
Technical counter ID
Month and year of count
"""
df = pd.read_csv("CyclingTrafficInParis_eng.csv")
df_counter = df.drop(["Hourly count","Date and time of count","Month and year of count","Geographic coordinates"], axis = 1)
df_counter.drop_duplicates(inplace = True)
df_counter.set_index("Counter name", inplace = True)

df.drop(["Counter ID","Counting site installation date","Geographic coordinates", "Counting site ID"],
        axis = 1,
        inplace = True) # Instead the Counters.csv from FirstPreparation.py could be used  

#grouping by the Counter name, aggregation by sum of hourly counts 
df = df.groupby(["Counter name"],as_index= True)["Hourly count"].sum()

#merge the previous df with the Counter metadata df
df_new = pd.concat([df, df_counter], axis=1)
df_new.set_index("Counter ID", inplace = True)

#generating a GeoDataFrame 
gdf = gpd.GeoDataFrame(
    df_new, geometry=gpd.points_from_xy(df_new.Longitude, df_new.Latitude), crs="EPSG:4326"
)

#creating a scatter plot on a map background
fig = px.scatter_mapbox(gdf,
                        lat=gdf.geometry.y,
                        lon=gdf.geometry.x,
                        size = "Hourly count",
                        color = "Hourly count",
                        hover_name="Counting site name",
                        hover_data="Hourly count",
                        color_continuous_scale=px.colors.sequential.Viridis,
                        zoom=12,
                        title = "Total counted bicycles in Paris")
#fig.update_layout(mapbox_style="open-street-map") #tried this, but it was too dificult to see the dots on the colored map background
fig.update_layout(mapbox_style="carto-positron") 
fig.update_layout(margin={"r":100,"t":100,"l":100,"b":100})
                    
fig.show()
