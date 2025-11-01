"""
Data preprocessing for asthma risk prediction
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess_weather_data(weather_data, aqi_data):
    """
    Preprocess weather and AQI data for model prediction
    
    Args:
        weather_data (dict): Weather data from OpenWeather API
        aqi_data (dict): Air quality data from AQI API
    
    Returns:
        np.array: Preprocessed features
    """
    # Extract weather features
    temperature = weather_data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    
    # Extract AQI features
    pm25 = aqi_data['list'][0]['components']['pm2_5']
    pm10 = aqi_data['list'][0]['components']['pm10']
    no2 = aqi_data['list'][0]['components']['no2']
    o3 = aqi_data['list'][0]['components']['o3']
    
    # For now, we'll use a simple approach without pollen data
    # In a real implementation, you might get pollen data from another API
    pollen = 50  # Placeholder value
    
    # Create feature array
    features = np.array([
        pm25,
        pm10,
        temperature,
        humidity,
        pollen
    ])
    
    return features

def normalize_features(features, scaler=None):
    """
    Normalize features using StandardScaler
    
    Args:
        features (np.array): Features to normalize
        scaler (StandardScaler, optional): Pre-fitted scaler
    
    Returns:
        tuple: (normalized_features, scaler)
    """
    if scaler is None:
        scaler = StandardScaler()
        normalized_features = scaler.fit_transform(features.reshape(1, -1))
    else:
        normalized_features = scaler.transform(features.reshape(1, -1))
    
    return normalized_features, scaler