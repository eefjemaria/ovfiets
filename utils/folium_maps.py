import streamlit as st
from streamlit_folium import folium_static
from preprocess.load_chargers_data import load_chargers_data
import folium
from folium.plugins.marker_cluster import MarkerCluster

def folium_map_charging_points(user:str):

    user_data = load_chargers_data(user)
    #Create map of NL
    m = folium.Map(
        location=[user_data.loc[0].position_lat, user_data.loc[0].position_lon],
        tiles='OpenStreetMap',
        zoom_start=13,
        prefer_canvas=True)

    for i in range(len(user_data)):
        lat, lon = user_data.iloc[i]['position_lat'], user_data.iloc[i]['position_lon']
        location = str(user_data.iloc[i]['poi_name'])
        address = str(user_data.iloc[i]['address_freeformAddress'])
        distance = str(round(user_data.iloc[i]['dist']))
        pp_text = '<b>Location: </b>' + location + '<br>' + '<b>Address: </b>' + address + '<br>' +'<b>Distance to home: </b>' + distance + ' meters'
        popup = folium.Popup(pp_text, min_width = 200, max_width=240)
        color = 'green'

        marker_cluster = MarkerCluster().add_to(m)

        folium.map.Marker(
            [lat, lon],
            popup = popup,
            icon=folium.Icon(icon='fa-plug', color=color, prefix='fa-solid'),
        ).add_to(marker_cluster)

    return m
