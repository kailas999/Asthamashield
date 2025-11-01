"""
Test script to verify enhanced asthma risk prediction models
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def test_enhanced_model():
    """Test the enhanced model training process"""
    print("🧪 Testing Enhanced Asthma Risk Prediction Model")
    print("=" * 50)
    
    # Load the dataset
    data_path = os.path.join('datasets', 'asthma_data.csv')
    if not os.path.exists(data_path):
        print("❌ Dataset not found. Please run the data generation script first.")
        return
    
    df = pd.read_csv(data_path)
    print(f"✅ Loaded dataset with {len(df)} samples")
    print(f"📊 Risk distribution: {dict(df['asthma_risk'].value_counts())}")
    
    # Prepare features and target
    feature_columns = ['pm25', 'pm10', 'temperature', 'humidity', 'pollen_level', 
                      'wind_speed', 'pressure', 'patient_age', 
                      'patient_history_severe_attacks', 'medication_adherence']
    X = df[feature_columns]
    y = df['asthma_risk']
    
    # Encode target labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"📊 Training set: {len(X_train)} samples")
    print(f"📊 Test set: {len(X_test)} samples")
    
    # Train a simple model for testing
    print("\n🧠 Training test model...")
    model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    accuracy = model.score(X_test, y_test)
    print(f"✅ Test accuracy: {accuracy:.4f}")
    
    # Test prediction
    print("\n🧪 Testing prediction...")
    test_sample = np.array([[92, 135, 31, 56, 50, 3.2, 1013, 35, 2, 0.8]])
    prediction_encoded = model.predict(test_sample)[0]
    prediction = le.inverse_transform([prediction_encoded])[0]
    
    print(f"📋 Test sample prediction: {prediction}")
    
    # Save test model and components
    print("\n💾 Saving test model components...")
    model_dir = os.path.join('asthmashield_app', 'ml_model')
    
    joblib.dump(model, os.path.join(model_dir, 'random_forest_model.pkl'))
    joblib.dump(le, os.path.join(model_dir, 'label_encoder.pkl'))
    joblib.dump(feature_columns, os.path.join(model_dir, 'feature_columns.pkl'))
    
    print("✅ Test model components saved successfully")
    print("\n🎉 Enhanced model test completed successfully!")

if __name__ == "__main__":
    test_enhanced_model()