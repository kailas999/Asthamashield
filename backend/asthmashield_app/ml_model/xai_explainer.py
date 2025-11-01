"""
Explainable AI (XAI) module for asthma risk prediction
Provides SHAP and LIME explanations for model predictions
"""

import numpy as np
import pandas as pd
import shap
import lime
import lime.lime_tabular
import os
import joblib
from .model import load_model

class XAIExplainer:
    def __init__(self, model_type='best'):
        """Initialize the XAI explainer with a trained model"""
        self.model, self.label_encoder, self.feature_columns = load_model(model_type)
        self.model_type = model_type
        self.explainer_shap = None
        self.explainer_lime = None
        
    def initialize_shap(self, X_sample=None):
        """Initialize SHAP explainer"""
        try:
            # For tree-based models, use TreeExplainer
            if hasattr(self.model.named_steps['classifier'], 'feature_importances_'):
                self.explainer_shap = shap.TreeExplainer(self.model.named_steps['classifier'])
            else:
                # For other models, use KernelExplainer with a sample of data
                if X_sample is not None:
                    self.explainer_shap = shap.KernelExplainer(
                        self.model.named_steps['classifier'].predict_proba, 
                        X_sample
                    )
                else:
                    # Create a small background dataset
                    background_data = np.random.rand(10, len(self.feature_columns))
                    self.explainer_shap = shap.KernelExplainer(
                        self.model.named_steps['classifier'].predict_proba, 
                        background_data
                    )
            return True
        except Exception as e:
            print(f"Error initializing SHAP explainer: {e}")
            return False
            
    def initialize_lime(self, training_data=None):
        """Initialize LIME explainer"""
        try:
            # Convert feature columns to list if needed
            feature_names = list(self.feature_columns) if hasattr(self.feature_columns, '__iter__') else self.feature_columns
            
            # Create LIME explainer
            self.explainer_lime = lime.lime_tabular.LimeTabularExplainer(
                training_data=training_data if training_data is not None else np.random.rand(100, len(feature_names)),
                feature_names=feature_names,
                class_names=self.label_encoder.classes_,
                mode='classification'
            )
            return True
        except Exception as e:
            print(f"Error initializing LIME explainer: {e}")
            return False
    
    def explain_shap(self, features):
        """Generate SHAP explanation for a prediction"""
        try:
            if self.explainer_shap is None:
                self.initialize_shap()
                
            # Apply preprocessing pipeline
            features_processed = self.model.named_steps['scaler'].transform([features])
            
            # Calculate SHAP values
            shap_values = self.explainer_shap.shap_values(features_processed)
            
            # Handle different SHAP output formats
            if isinstance(shap_values, list):
                # For multi-class, return explanation for predicted class
                prediction = self.model.predict([features])[0]
                class_idx = prediction  # Already encoded
                shap_vals = shap_values[class_idx]
            else:
                shap_vals = shap_values
                
            # Create feature importance dictionary
            feature_importance = dict(zip(self.feature_columns, shap_vals[0]))
            
            return {
                'explanation_method': 'SHAP',
                'feature_importance': feature_importance,
                'shap_values': shap_vals[0].tolist() if hasattr(shap_vals[0], 'tolist') else shap_vals[0]
            }
        except Exception as e:
            return {
                'error': f"SHAP explanation failed: {str(e)}",
                'explanation_method': 'SHAP'
            }
    
    def explain_lime(self, features, num_features=10):
        """Generate LIME explanation for a prediction"""
        try:
            if self.explainer_lime is None:
                self.initialize_lime()
                
            def predict_fn(x):
                # Apply same preprocessing as training
                x_scaled = self.model.named_steps['scaler'].transform(x)
                return self.model.named_steps['classifier'].predict_proba(x_scaled)
            
            # Generate LIME explanation
            exp = self.explainer_lime.explain_instance(
                features, 
                predict_fn, 
                num_features=num_features,
                top_labels=1
            )
            
            # Get explanation for the top predicted class
            prediction = self.model.predict([features])[0]
            class_label = self.label_encoder.inverse_transform([prediction])[0]
            
            # Extract feature weights
            explanation = exp.as_list(label=prediction)
            feature_weights = dict(explanation)
            
            return {
                'explanation_method': 'LIME',
                'predicted_class': class_label,
                'feature_weights': feature_weights,
                'explanation': explanation
            }
        except Exception as e:
            return {
                'error': f"LIME explanation failed: {str(e)}",
                'explanation_method': 'LIME'
            }

def get_xai_explanation(pm25, pm10, temperature, humidity, pollen_level, 
                       wind_speed, pressure, patient_age, 
                       patient_history_severe_attacks, medication_adherence,
                       method='both'):
    """Get XAI explanation for asthma risk prediction"""
    try:
        # Prepare features
        features = [
            pm25, pm10, temperature, humidity, pollen_level, 
            wind_speed, pressure, patient_age, 
            patient_history_severe_attacks, medication_adherence
        ]
        
        # Initialize explainer
        explainer = XAIExplainer()
        
        explanations = {}
        
        if method in ['shap', 'both']:
            shap_explanation = explainer.explain_shap(features)
            explanations['shap'] = shap_explanation
            
        if method in ['lime', 'both']:
            lime_explanation = explainer.explain_lime(features)
            explanations['lime'] = lime_explanation
            
        return explanations
    except Exception as e:
        return {'error': f"XAI explanation failed: {str(e)}"}

# For testing purposes
if __name__ == "__main__":
    # Test XAI explanation
    try:
        explanations = get_xai_explanation(
            pm25=92, pm10=135, temperature=31, humidity=56, pollen_level=50,
            wind_speed=3.2, pressure=1013, patient_age=35, 
            patient_history_severe_attacks=2, medication_adherence=0.8
        )
        print("XAI Explanations:")
        for method, explanation in explanations.items():
            print(f"\n{method.upper()} Explanation:")
            print(explanation)
    except Exception as e:
        print(f"Error: {e}")