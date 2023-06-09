import pandas as pd
import folium
from folium.plugins import HeatMap
import ast

# Load Airbnb data from CSV
airbnb_df = pd.read_csv('airbnb_data.csv', on_bad_lines='warn')

# Convert the location string to a dictionary and extract lat and lng values
airbnb_df['location'] = airbnb_df['location'].apply(ast.literal_eval)
airbnb_df['lat'] = airbnb_df['location'].apply(lambda x: x['lat'])
airbnb_df['lng'] = airbnb_df['location'].apply(lambda x: x['lng'])

# Load Booking data from CSV
booking_df = pd.read_csv('booking_data.csv', on_bad_lines='warn')
booking_df['location'] = booking_df['location'].apply(ast.literal_eval)
booking_df['lat'] = booking_df['location'].apply(lambda x: x['lat'])
booking_df['lng'] = booking_df['location'].apply(lambda x: x['lng'])

# Specify the base map
base_map = folium.Map(location=[39.6249838, 19.9223461], control_scale=True, zoom_start=11)

# Create a FeatureGroup for Airbnb Heatmap and add it to the map
airbnb_heatmap = folium.FeatureGroup(name='Airbnb Heatmap', show=True).add_to(base_map)
HeatMap(data=airbnb_df[['lat', 'lng']].values, radius=8, max_zoom=13).add_to(airbnb_heatmap)

# Create a FeatureGroup for Airbnb Markers and add it to the map
airbnb_markers = folium.FeatureGroup(name='Airbnb Markers', show=True).add_to(base_map)

# Add Airbnb markers to the map
for idx, row in airbnb_df.iterrows():
    location = (row['lat'], row['lng'])
    listing_name = row.get('name', 'N/A')
    rating = row.get('stars', 'N/A')
    url = row.get('url', 'N/A')
    folium.Marker(location, popup=f'<b>Name:</b> {listing_name}<br><b>Rating:</b> {rating}<br><b>URL:</b> <a href={url} target="_blank">Link</a>').add_to(airbnb_markers)

# Create a FeatureGroup for Booking Markers with a different color
booking_markers = folium.FeatureGroup(name='Booking Markers', show=True).add_to(base_map)

# Add Booking markers to the map
for idx, row in booking_df.iterrows():
    location = (row['lat'], row['lng'])
    listing_name = row.get('name', 'N/A')
    rating = row.get('rating', 'N/A')
    url = row.get('url', 'N/A')
    folium.Marker(location, popup=f'<b>Name:</b> {listing_name}<br><b>Rating:</b> {rating}<br><b>URL:</b> <a href={url} target="_blank">Link</a>', icon=folium.Icon(color='red')).add_to(booking_markers)

# Create a FeatureGroup for Booking Heatmap and add it to the map
booking_heatmap = folium.FeatureGroup(name='Booking Heatmap', show=True).add_to(base_map)
HeatMap(data=booking_df[['lat', 'lng']].values, radius=8, max_zoom=13, gradient={0.0: 'blue', 0.0: 'green', 1.0: 'red'}).add_to(booking_heatmap)

# Add LayerControl to the map
folium.LayerControl(collapsed=False, overlay=True).add_to(base_map)

# Save the map to an HTML file
base_map.save('heatmap.html')
