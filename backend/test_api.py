#!/usr/bin/env python
"""
Test script for AsthmaShield backend API
"""

import requests
import json

def test_api():
    """Test the AsthmaShield backend API"""
    base_url = "http://localhost:8000/api"
    
    # Test the predict endpoint with patient data
    print("Testing predict endpoint with patient data...")
    try:
        params = {
            'city': 'Pune',
            'patient_age': 35,
            'patient_history_severe_attacks': 2,
            'medication_adherence': 0.8
        }
        response = requests.get(f"{base_url}/predict/", params=params)
        if response.status_code == 200:
            data = response.json()
            print("API Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error connecting to API: {e}")

if __name__ == "__main__":
    test_api()