"""
Map component for AsthmaShield
"""

import folium
from streamlit_folium import st_folium

def create_risk_map(center_lat=20.5937, center_lon=78.9629, zoom=5):
    """
    Create a risk map using OpenStreetMap and Leaflet.js
    
    Args:
        center_lat (float): Center latitude
        center_lon (float): Center longitude
        zoom (int): Initial zoom level
    
    Returns:
        folium.Map: Configured map object
    """
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def add_city_marker(map_obj, lat, lon, city_name, risk_level, popup_info=None):
    """
    Add a city marker with risk level to the map
    
    Args:
        map_obj (folium.Map): Map object
        lat (float): Latitude
        lon (float): Longitude
        city_name (str): Name of the city
        risk_level (str): Risk level (High, Moderate, Low)
        popup_info (dict): Additional information for popup
    """
    # Define colors based on risk level
    color_map = {
        'High': 'red',
        'Moderate': 'orange',
        'Low': 'green'
    }
    
    color = color_map.get(risk_level, 'blue')
    
    # Create popup content
    popup_content = f"<b>{city_name}</b><br>Risk Level: {risk_level}"
    if popup_info:
        popup_content += f"<br>PM2.5: {popup_info.get('pm25', 'N/A')}"
        popup_content += f"<br>Temperature: {popup_info.get('temperature', 'N/A')}°C"
    
    # Add marker
    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        popup=popup_content,
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.6
    ).add_to(map_obj)

def display_map(map_obj, width=700, height=500):
    """
    Display the map in Streamlit
    
    Args:
        map_obj (folium.Map): Map object to display
        width (int): Width of the map
        height (int): Height of the map
    """
    st_folium(map_obj, width=width, height=height)