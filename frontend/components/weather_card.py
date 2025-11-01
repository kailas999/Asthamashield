"""
Weather card component for displaying environmental data
"""

import streamlit as st

def display_weather_card(title, value, unit="", icon="", color="blue"):
    """
    Display a weather data card
    
    Args:
        title (str): Card title
        value (float/str): Value to display
        unit (str): Unit of measurement
        icon (str): Emoji or icon to display
        color (str): Color for the card
    """
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
        <h4>{icon} {title}</h4>
        <p style="font-size: 1.5rem; font-weight: bold; color: {color};">{value} {unit}</p>
    </div>
    """, unsafe_allow_html=True)

def display_risk_card(risk_level):
    """
    Display asthma risk level card
    
    Args:
        risk_level (str): Risk level (High, Moderate, Low)
    """
    risk_colors = {
        'High': '#f44336',
        'Moderate': '#ff9800',
        'Low': '#4caf50'
    }
    
    risk_emojis = {
        'High': '🔴',
        'Moderate': '🟠',
        'Low': '🟢'
    }
    
    color = risk_colors.get(risk_level, '#2196f3')
    emoji = risk_emojis.get(risk_level, '🔵')
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; 
                border-left: 5px solid {color}; margin: 1rem 0;">
        <h2 style="color: {color};">{emoji} {risk_level} Risk</h2>
        <p>{get_risk_description(risk_level)}</p>
    </div>
    """, unsafe_allow_html=True)

def get_risk_description(risk_level):
    """
    Get description for risk level
    
    Args:
        risk_level (str): Risk level
    
    Returns:
        str: Description of the risk level
    """
    descriptions = {
        'High': 'Air quality is unhealthy. Take precautions and consider staying indoors.',
        'Moderate': 'Air quality is acceptable but may affect sensitive individuals.',
        'Low': 'Air quality is good for most individuals.'
    }
    
    return descriptions.get(risk_level, 'Unknown risk level')