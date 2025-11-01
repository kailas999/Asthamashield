"""
Script to generate a comprehensive report of ML models
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def generate_model_report():
    """Generate a comprehensive report of ML models"""
    # Load the dataset
    data_path = os.path.join('datasets', 'asthma_data.csv')
    df = pd.read_csv(data_path)
    
    # Prepare features and target
    feature_columns = ['pm25', 'pm10', 'temperature', 'humidity', 'pollen_level', 
                      'wind_speed', 'pressure', 'patient_age', 
                      'patient_history_severe_attacks', 'medication_adherence']
    X = df[feature_columns]
    y = df['asthma_risk']
    
    # Encode target labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Initialize models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
    }
    
    # Generate report
    print("Asthma Risk Prediction Model Report")
    print("=" * 50)
    print(f"Dataset size: {len(df)} samples")
    print(f"Features: {len(feature_columns)}")
    print(f"Classes: {list(le.classes_)}")
    print()
    
    # Evaluate each model
    for name, model in models.items():
        print(f"{name} Model Evaluation")
        print("-" * 30)
        
        # Cross-validation scores
        cv_scores = cross_val_score(model, X, y_encoded, cv=5)
        print(f"Cross-validation scores: {cv_scores}")
        print(f"Mean CV score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        # Fit model and get detailed report
        model.fit(X, y_encoded)
        y_pred = model.predict(X)
        print("\nClassification Report:")
        print(classification_report(y_encoded, y_pred, target_names=le.classes_))
        
        # Feature importance (for tree-based models)
        if hasattr(model, 'feature_importances_'):
            print("\nFeature Importance:")
            feature_importance = pd.DataFrame({
                'feature': feature_columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            print(feature_importance.to_string(index=False))
        
        print("\n" + "="*50 + "\n")
    
    # Save model comparison
    comparison_data = []
    for name, model in models.items():
        cv_scores = cross_val_score(model, X, y_encoded, cv=5)
        comparison_data.append({
            'Model': name,
            'Mean CV Score': cv_scores.mean(),
            'Std CV Score': cv_scores.std()
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    print("Model Comparison:")
    print(comparison_df.to_string(index=False))

if __name__ == "__main__":
    generate_model_report()