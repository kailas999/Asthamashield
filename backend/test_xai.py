"""
Test script for XAI explanations in asthma risk prediction
"""

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from asthmashield_app.ml_model.xai_explainer import XAIExplainer

def test_xai_explanations():
    """Test XAI explanations with sample data"""
    print("Testing XAI explanations...")
    
    # Sample features
    sample_features = [
        92,   # pm25
        135,  # pm10
        31,   # temperature
        56,   # humidity
        50,   # pollen_level
        3.2,  # wind_speed
        1013, # pressure
        35,   # patient_age
        2,    # patient_history_severe_attacks
        0.8   # medication_adherence
    ]
    
    try:
        # Initialize explainer
        explainer = XAIExplainer()
        print("XAIExplainer initialized successfully")
        
        # Test SHAP explanation
        print("\nTesting SHAP explanation...")
        shap_result = explainer.explain_shap(sample_features)
        if 'error' not in shap_result:
            print("SHAP explanation successful!")
            print("Top features:")
            if 'feature_importance' in shap_result and isinstance(shap_result['feature_importance'], dict):
                feature_importance = shap_result['feature_importance']
                sorted_features = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
                for feature, importance in sorted_features[:5]:
                    print(f"  {feature}: {importance:.4f}")
            else:
                print("  Feature importance data not available in expected format")
        else:
            print(f"SHAP explanation failed: {shap_result['error']}")
        
        # Test LIME explanation
        print("\nTesting LIME explanation...")
        lime_result = explainer.explain_lime(sample_features)
        if 'error' not in lime_result:
            print("LIME explanation successful!")
            print("Predicted class:", lime_result.get('predicted_class', 'Unknown'))
            print("Top features:")
            if 'feature_weights' in lime_result and isinstance(lime_result['feature_weights'], dict):
                feature_weights = lime_result['feature_weights']
                sorted_features = sorted(feature_weights.items(), key=lambda x: abs(x[1]), reverse=True)
                for feature, weight in sorted_features[:5]:
                    print(f"  {feature}: {weight:.4f}")
            else:
                print("  Feature weights data not available in expected format")
        else:
            print(f"LIME explanation failed: {lime_result['error']}")
            
    except Exception as e:
        print(f"Error testing XAI explanations: {str(e)}")

if __name__ == "__main__":
    test_xai_explanations()