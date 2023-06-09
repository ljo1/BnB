import pandas as pd
import folium
from folium.plugins import HeatMap
import ast
from folium.map import Layer, FeatureGroup
from folium import plugins

df = pd.read_csv('airbnb_data.csv', on_bad_lines='warn')

# Convert the string dictionary to a dictionary and extract lat and lng values
df['location'] = df['location'].apply(ast.literal_eval)
df['lat'] = df['location'].apply(lambda x: x['lat'])
df['lng'] = df['location'].apply(lambda x: x['lng'])

# Specify a base map
base_map = folium.Map(location=[39.6249838, 19.9223461], control_scale=True, zoom_start=11)

# Create a FeatureGroup for Heatmap and add it to the map
heatmap = FeatureGroup(name='Heat Map', show=False).add_to(base_map)
HeatMap(data=list(zip(df['lat'].values, df['lng'].values)), radius=8, max_zoom=13).add_to(heatmap)

# Create a FeatureGroup for Markers and add it to the map
markers = FeatureGroup(name='Markers', show=True).add_to(base_map)

# Add markers to the map
for idx, row in df.iterrows():
    location = (row['lat'], row['lng'])
    listing_name = row.get('name', 'N/A')  # replace 'listing_name' with actual column name
    rating = row.get('stars', 'N/A')  # replace 'rating' with actual column name
    url = row.get('url', 'N/A')  # replace 'url' with actual column name
    folium.Marker(location, popup=f'<b>Name:</b> {listing_name}<br><b>Rating:</b> {rating}<br><b>URL:</b> <a href={url} target="_blank">Link</a>').add_to(markers)

# Add a LayerControl object to the map to enable toggling between Heatmap and Markers
folium.LayerControl().add_to(base_map)

# Save the map to an HTML file
base_map.save('heatmap.html')
