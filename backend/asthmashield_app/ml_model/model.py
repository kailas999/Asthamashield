"""
ML model for asthma risk prediction with enhanced accuracy
"""

import numpy as np
import joblib
import os

def load_model(model_type='best'):
    """Load the trained model and related components"""
    try:
        model_dir = os.path.dirname(__file__)
        
        # Try to load specific model type first
        model_filename = f'{model_type.lower().replace(" ", "_")}_model.pkl'
        model_path = os.path.join(model_dir, model_filename)
        
        # If specific model doesn't exist, try to load the best model
        if not os.path.exists(model_path):
            model_path = os.path.join(model_dir, 'random_forest_model.pkl')
        
        encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
        feature_path = os.path.join(model_dir, 'feature_columns.pkl')
        
        model = joblib.load(model_path)
        label_encoder = joblib.load(encoder_path)
        feature_columns = joblib.load(feature_path)
        
        return model, label_encoder, feature_columns
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Model files not found. Please train the model first using train_model.py. Error: {e}")

def predict_asthma_risk(pm25, pm10, temperature, humidity, pollen_level, 
                       wind_speed, pressure, patient_age, 
                       patient_history_severe_attacks, medication_adherence,
                       model_type='best', include_xai=False):
    """Predict asthma risk level with enhanced accuracy"""
    try:
        model, label_encoder, feature_columns = load_model(model_type)
        
        # Prepare features in the correct order
        features = np.array([[
            pm25, pm10, temperature, humidity, pollen_level, 
            wind_speed, pressure, patient_age, 
            patient_history_severe_attacks, medication_adherence
        ]])
        
        # Make prediction
        prediction_encoded = model.predict(features)[0]
        
        # Get prediction probabilities if available
        probabilities = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)[0]
        
        # Decode prediction
        prediction = label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Create confidence score
        confidence = max(probabilities) if probabilities is not None else None
        
        result = {
            'risk_level': prediction,
            'confidence': confidence,
            'probabilities': dict(zip(label_encoder.classes_, probabilities)) if probabilities is not None else None
        }
        
        # Add XAI explanations if requested
        if include_xai:
            try:
                from .xai_explainer import get_xai_explanation
                xai_explanations = get_xai_explanation(
                    pm25, pm10, temperature, humidity, pollen_level, 
                    wind_speed, pressure, patient_age, 
                    patient_history_severe_attacks, medication_adherence,
                    method='both'
                )
                result['xai_explanations'] = xai_explanations
            except Exception as e:
                result['xai_error'] = str(e)
        
        return result
    except Exception as e:
        raise Exception(f"Error during prediction: {str(e)}")

def get_feature_importance(model_type='best'):
    """Get feature importance from the trained model (if available)"""
    try:
        model, label_encoder, feature_columns = load_model(model_type)
        
        # Check if model has feature importance
        if hasattr(model.named_steps['classifier'], 'feature_importances_'):
            importances = model.named_steps['classifier'].feature_importances_
            feature_importance = dict(zip(feature_columns, importances))
            return feature_importance
        else:
            return None
    except Exception as e:
        return None

# For testing purposes
if __name__ == "__main__":
    # This will only work if the model has been trained
    try:
        result = predict_asthma_risk(
            pm25=92, pm10=135, temperature=31, humidity=56, pollen_level=50,
            wind_speed=3.2, pressure=1013, patient_age=35, 
            patient_history_severe_attacks=2, medication_adherence=0.8,
            include_xai=True
        )
        print(f"Predicted risk: {result['risk_level']}")
        if result['confidence']:
            print(f"Confidence: {result['confidence']:.2f}")
        if result['probabilities']:
            print("Probabilities:")
            for risk, prob in result['probabilities'].items():
                print(f"  {risk}: {prob:.2f}")
        if 'xai_explanations' in result:
            print("\nXAI Explanations:")
            for method, explanation in result['xai_explanations'].items():
                print(f"\n{method.upper()}:")
                print(explanation)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Prediction error: {e}")