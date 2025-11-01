"""
Test script for model loading and prediction
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from asthmashield_app.ml_model.model import predict_asthma_risk

def test_model_prediction():
    """Test model prediction with sample data"""
    print("Testing model prediction...")
    
    try:
        # Sample features
        result = predict_asthma_risk(
            pm25=92, pm10=135, temperature=31, humidity=56, pollen_level=50,
            wind_speed=3.2, pressure=1013, patient_age=35, 
            patient_history_severe_attacks=2, medication_adherence=0.8,
            include_xai=True
        )
        
        print("Prediction successful!")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Confidence: {result['confidence']}")
        
        if 'xai_explanations' in result:
            print("XAI explanations available:")
            xai = result['xai_explanations']
            if 'shap' in xai:
                print("  SHAP explanation available")
            if 'lime' in xai:
                print("  LIME explanation available")
        else:
            print("No XAI explanations available")
            
    except Exception as e:
        print(f"Error testing model prediction: {str(e)}")

if __name__ == "__main__":
    test_model_prediction()