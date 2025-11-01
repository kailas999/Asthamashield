"""
Script to demonstrate adding new data to the asthma dataset
"""

import pandas as pd
import random

def add_new_data():
    """Demonstrate adding new data to the dataset"""
    # Load existing dataset
    df = pd.read_csv('datasets/asthma_data.csv')
    print(f"Original dataset size: {len(df)} samples")
    
    # Generate new sample data
    new_data = []
    for i in range(5):  # Add 5 new samples
        sample = {
            'pm25': round(random.uniform(0, 300), 1),
            'pm10': round(random.uniform(0, 400), 1),
            'temperature': round(random.uniform(-10, 50), 1),
            'humidity': round(random.uniform(0, 100), 1),
            'pollen_level': round(random.uniform(0, 100), 1),
            'wind_speed': round(random.uniform(0, 20), 1),
            'pressure': round(random.uniform(980, 1040), 1),
            'patient_age': random.randint(5, 80),
            'patient_history_severe_attacks': random.randint(0, 10),
            'medication_adherence': round(random.uniform(0.5, 1.0), 2),
            'asthma_risk': random.choice(['Low', 'Moderate', 'High'])
        }
        new_data.append(sample)
    
    # Convert to DataFrame
    new_df = pd.DataFrame(new_data)
    
    # Combine with existing data
    combined_df = pd.concat([df, new_df], ignore_index=True)
    
    # Save updated dataset
    combined_df.to_csv('datasets/asthma_data.csv', index=False)
    
    print(f"Added {len(new_df)} new samples")
    print(f"Updated dataset size: {len(combined_df)} samples")
    print("\nNew samples added:")
    print(new_df)
    
    print("\nDataset updated successfully!")

if __name__ == "__main__":
    add_new_data()