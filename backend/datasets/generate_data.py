"""
Script to generate realistic and diverse asthma training data for different cities
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime

def generate_city_data():
    """Define realistic data ranges for different cities"""
    cities_data = {
        'Delhi': {
            'pm25_range': (100, 500),
            'pm10_range': (150, 600),
            'humidity_range': (30, 80),
            'temperature_range': (15, 45),
            'pollen_range': (40, 90),
            'base_risk': 'High'
        },
        'Mumbai': {
            'pm25_range': (50, 200),
            'pm10_range': (80, 300),
            'humidity_range': (60, 90),
            'temperature_range': (20, 35),
            'pollen_range': (30, 70),
            'base_risk': 'Moderate'
        },
        'Bangalore': {
            'pm25_range': (30, 100),
            'pm10_range': (50, 150),
            'humidity_range': (40, 70),
            'temperature_range': (15, 30),
            'pollen_range': (20, 60),
            'base_risk': 'Low'
        },
        'Chennai': {
            'pm25_range': (40, 150),
            'pm10_range': (60, 200),
            'humidity_range': (50, 85),
            'temperature_range': (25, 40),
            'pollen_range': (25, 65),
            'base_risk': 'Moderate'
        },
        'Kolkata': {
            'pm25_range': (80, 300),
            'pm10_range': (120, 400),
            'humidity_range': (55, 85),
            'temperature_range': (18, 38),
            'pollen_range': (35, 75),
            'base_risk': 'Moderate'
        },
        'Hyderabad': {
            'pm25_range': (45, 180),
            'pm10_range': (70, 250),
            'humidity_range': (35, 75),
            'temperature_range': (20, 42),
            'pollen_range': (30, 70),
            'base_risk': 'Moderate'
        },
        'Pune': {
            'pm25_range': (30, 120),
            'pm10_range': (50, 180),
            'humidity_range': (40, 75),
            'temperature_range': (15, 35),
            'pollen_range': (25, 65),
            'base_risk': 'Low'
        },
        'Ahmedabad': {
            'pm25_range': (120, 400),
            'pm10_range': (180, 500),
            'humidity_range': (25, 70),
            'temperature_range': (18, 45),
            'pollen_range': (45, 85),
            'base_risk': 'High'
        },
        'Jaipur': {
            'pm25_range': (90, 300),
            'pm10_range': (140, 400),
            'humidity_range': (20, 65),
            'temperature_range': (10, 45),
            'pollen_range': (40, 80),
            'base_risk': 'Moderate'
        },
        'Lucknow': {
            'pm25_range': (110, 350),
            'pm10_range': (160, 450),
            'humidity_range': (35, 80),
            'temperature_range': (12, 42),
            'pollen_range': (45, 85),
            'base_risk': 'High'
        }
    }
    return cities_data

def generate_realistic_sample(city_data, base_risk, patient_age=None):
    """Generate a realistic sample based on city data and risk factors"""
    # Generate patient data
    if patient_age is None:
        patient_age = random.randint(5, 80)
    
    patient_history_severe_attacks = random.randint(0, 10)
    medication_adherence = random.uniform(0.5, 1.0)
    
    # Get city-specific environmental data ranges
    pm25_min, pm25_max = city_data['pm25_range']
    pm10_min, pm10_max = city_data['pm10_range']
    humidity_min, humidity_max = city_data['humidity_range']
    temp_min, temp_max = city_data['temperature_range']
    pollen_min, pollen_max = city_data['pollen_range']
    
    # Generate environmental data
    pm25 = random.uniform(pm25_min, pm25_max)
    pm10 = random.uniform(pm10_min, pm10_max)
    humidity = random.uniform(humidity_min, humidity_max)
    temperature = random.uniform(temp_min, temp_max)
    pollen_level = random.uniform(pollen_min, pollen_max)
    wind_speed = random.uniform(0.5, 15.0)
    pressure = random.uniform(990, 1030)
    
    # Adjust risk based on environmental and patient factors
    env_risk_score = 0
    if pm25 > 150 or pm10 > 200:
        env_risk_score += 2
    elif pm25 > 75 or pm10 > 125:
        env_risk_score += 1
        
    if temperature < 5 or temperature > 40:
        env_risk_score += 1
        
    if humidity < 30 or humidity > 80:
        env_risk_score += 1
        
    if pollen_level > 70:
        env_risk_score += 2
    elif pollen_level > 40:
        env_risk_score += 1
    
    # Patient risk factors
    patient_risk_score = 0
    if patient_age < 10 or patient_age > 65:
        patient_risk_score += 1
        
    if patient_history_severe_attacks > 3:
        patient_risk_score += 2
    elif patient_history_severe_attacks > 1:
        patient_risk_score += 1
        
    if medication_adherence < 0.7:
        patient_risk_score += 2
    elif medication_adherence < 0.9:
        patient_risk_score += 1
    
    # Combine scores to determine risk level
    total_risk_score = env_risk_score + patient_risk_score
    
    # Adjust based on city's base risk
    if city_data['base_risk'] == 'High':
        total_risk_score += 1
    elif city_data['base_risk'] == 'Low':
        total_risk_score -= 1
    
    # Determine final risk level
    if total_risk_score >= 4:
        asthma_risk = 'High'
    elif total_risk_score >= 2:
        asthma_risk = 'Moderate'
    else:
        asthma_risk = 'Low'
    
    return {
        'pm25': round(pm25, 1),
        'pm10': round(pm10, 1),
        'temperature': round(temperature, 1),
        'humidity': round(humidity, 1),
        'pollen_level': round(pollen_level, 1),
        'wind_speed': round(wind_speed, 1),
        'pressure': round(pressure, 1),
        'patient_age': patient_age,
        'patient_history_severe_attacks': patient_history_severe_attacks,
        'medication_adherence': round(medication_adherence, 2),
        'asthma_risk': asthma_risk
    }

def generate_diverse_dataset(n_samples_per_city=200):
    """Generate a diverse dataset with samples from different cities and risk levels"""
    cities_data = generate_city_data()
    data = []
    
    # Generate samples for each city
    for city, city_data in cities_data.items():
        print(f"Generating data for {city}...")
        
        # Generate samples for this city
        for _ in range(n_samples_per_city):
            sample = generate_realistic_sample(city_data, city_data['base_risk'])
            data.append(sample)
        
        # Generate some samples with different patient profiles for the same city
        for _ in range(50):
            # Young patient
            sample = generate_realistic_sample(city_data, city_data['base_risk'], patient_age=random.randint(5, 18))
            data.append(sample)
            
            # Elderly patient
            sample = generate_realistic_sample(city_data, city_data['base_risk'], patient_age=random.randint(65, 80))
            data.append(sample)
            
            # Patient with severe history
            sample = generate_realistic_sample(city_data, city_data['base_risk'])
            sample['patient_history_severe_attacks'] = random.randint(4, 10)
            # Recalculate risk based on new patient profile
            if sample['asthma_risk'] != 'High':
                sample['asthma_risk'] = 'Moderate' if sample['asthma_risk'] == 'Low' else 'High'
            data.append(sample)
            
            # Patient with poor medication adherence
            sample = generate_realistic_sample(city_data, city_data['base_risk'])
            sample['medication_adherence'] = random.uniform(0.3, 0.7)
            # Recalculate risk based on new patient profile
            if sample['asthma_risk'] != 'High':
                sample['asthma_risk'] = 'Moderate' if sample['asthma_risk'] == 'Low' else 'High'
            data.append(sample)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Shuffle the data
    df = df.sample(frac=1).reset_index(drop=True)
    
    print(f"Generated {len(df)} samples from {len(cities_data)} cities")
    print(f"Risk distribution:\n{df['asthma_risk'].value_counts()}")
    
    return df

def save_data(df, filename='asthma_data_enhanced.csv'):
    """Save data to CSV file"""
    filepath = os.path.join('datasets', filename)
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")

def combine_with_existing_data(new_df):
    """Combine new data with existing dataset"""
    try:
        # Load existing data
        existing_path = os.path.join('datasets', 'asthma_data.csv')
        existing_df = pd.read_csv(existing_path)
        
        # Combine datasets
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # Remove duplicates
        combined_df = combined_df.drop_duplicates()
        
        # Save combined dataset
        combined_df.to_csv(existing_path, index=False)
        print(f"Combined dataset saved to {existing_path}")
        print(f"Total samples: {len(combined_df)}")
        print(f"Risk distribution:\n{combined_df['asthma_risk'].value_counts()}")
        
        return combined_df
    except FileNotFoundError:
        # If no existing data, just save the new data
        new_df.to_csv(os.path.join('datasets', 'asthma_data.csv'), index=False)
        print("Created new dataset file")
        return new_df

if __name__ == "__main__":
    import os
    
    print("Generating enhanced asthma dataset...")
    
    # Generate diverse dataset
    df = generate_diverse_dataset(n_samples_per_city=300)
    
    # Combine with existing data
    combined_df = combine_with_existing_data(df)
    
    print("\nDataset generation completed successfully!")