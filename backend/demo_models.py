"""
Script to demonstrate using different ML models for asthma risk prediction
"""

import numpy as np
from asthmashield_app.ml_model.model import predict_asthma_risk

def demo_models():
    """Demonstrate different ML models"""
    # Sample patient and environmental data
    sample_data = {
        'pm25': 92.0,
        'pm10': 135.0,
        'temperature': 31.0,
        'humidity': 56.0,
        'pollen_level': 50.0,
        'wind_speed': 3.2,
        'pressure': 1013.0,
        'patient_age': 35,
        'patient_history_severe_attacks': 2,
        'medication_adherence': 0.8
    }
    
    print("Asthma Risk Prediction Demo")
    print("=" * 40)
    print(f"Environmental Data:")
    print(f"  PM2.5: {sample_data['pm25']} μg/m³")
    print(f"  PM10: {sample_data['pm10']} μg/m³")
    print(f"  Temperature: {sample_data['temperature']}°C")
    print(f"  Humidity: {sample_data['humidity']}%")
    print(f"  Wind Speed: {sample_data['wind_speed']} m/s")
    print(f"  Pressure: {sample_data['pressure']} hPa")
    print(f"  Pollen Level: {sample_data['pollen_level']}")
    print()
    print(f"Patient Data:")
    print(f"  Age: {sample_data['patient_age']} years")
    print(f"  History of Severe Attacks: {sample_data['patient_history_severe_attacks']}")
    print(f"  Medication Adherence: {sample_data['medication_adherence']*100:.0f}%")
    print()
    
    # Test different models
    models = ['random_forest', 'logistic_regression']
    
    for model_type in models:
        try:
            print(f"Prediction using {model_type.replace('_', ' ').title()}:")
            risk = predict_asthma_risk(
                pm25=sample_data['pm25'],
                pm10=sample_data['pm10'],
                temperature=sample_data['temperature'],
                humidity=sample_data['humidity'],
                pollen_level=sample_data['pollen_level'],
                wind_speed=sample_data['wind_speed'],
                pressure=sample_data['pressure'],
                patient_age=sample_data['patient_age'],
                patient_history_severe_attacks=sample_data['patient_history_severe_attacks'],
                medication_adherence=sample_data['medication_adherence'],
                model_type=model_type
            )
            print(f"  Predicted Risk Level: {risk}")
            print()
        except FileNotFoundError:
            print(f"  Model '{model_type}' not found. Please train the model first.")
            print()

if __name__ == "__main__":
    demo_models()