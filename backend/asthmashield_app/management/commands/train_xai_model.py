"""
Management command to train asthma risk prediction models with XAI capabilities
"""

from django.core.management.base import BaseCommand
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

class Command(BaseCommand):
    help = 'Train asthma risk prediction models with XAI capabilities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            default='best',
            choices=['best', 'random_forest', 'logistic_regression', 'gradient_boosting', 'svm'],
            help='Model type to train'
        )
        
        parser.add_argument(
            '--no-augment',
            action='store_true',
            help='Disable data augmentation'
        )
        
        parser.add_argument(
            '--xai-validation',
            action='store_true',
            help='Perform XAI validation on trained model'
        )

    def handle(self, *args, **options):
        model_type = options['model']
        augment_data = not options['no_augment']
        xai_validation = options['xai_validation']
        
        self.stdout.write(f'Starting training for {model_type} model...')
        
        try:
            # Import the train_model function
            from ....train_model import train_model
            
            # Train the model
            model, label_encoder = train_model(model_type, augment_data)
            
            if model is None:
                self.stdout.write('Model training failed!')
                return
            
            self.stdout.write('Model training completed successfully!')
            
            # Perform XAI validation if requested
            if xai_validation:
                self.stdout.write('Performing XAI validation...')
                self.perform_xai_validation(model, label_encoder)
                
        except Exception as e:
            self.stdout.write(f'Error during training: {str(e)}')
    
    def perform_xai_validation(self, model, label_encoder):
        """Perform XAI validation on the trained model"""
        try:
            # Import XAI explainer
            from ...ml_model.xai_explainer import XAIExplainer
            
            # Initialize explainer
            explainer = XAIExplainer()
            
            # Test with sample data
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
            
            # Test SHAP explanation
            shap_result = explainer.explain_shap(sample_features)
            if 'error' not in shap_result:
                self.stdout.write('SHAP explanation test passed!')
            else:
                self.stdout.write(f'SHAP explanation test failed: {shap_result["error"]}')
            
            # Test LIME explanation
            lime_result = explainer.explain_lime(sample_features)
            if 'error' not in lime_result:
                self.stdout.write('LIME explanation test passed!')
            else:
                self.stdout.write(f'LIME explanation test failed: {lime_result["error"]}')
                
        except Exception as e:
            self.stdout.write(f'XAI validation failed: {str(e)}')