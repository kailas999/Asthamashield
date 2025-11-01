"""
Script to train the asthma risk prediction model with enhanced accuracy
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os
import argparse
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data():
    """Load and preprocess the asthma dataset"""
    # Load the dataset
    data_path = os.path.join('datasets', 'asthma_data.csv')
    df = pd.read_csv(data_path)
    
    # Display basic info
    print(f"Dataset shape: {df.shape}")
    print(f"Risk distribution:\n{df['asthma_risk'].value_counts()}")
    
    # Prepare features and target
    feature_columns = ['pm25', 'pm10', 'temperature', 'humidity', 'pollen_level', 
                      'wind_speed', 'pressure', 'patient_age', 
                      'patient_history_severe_attacks', 'medication_adherence']
    X = df[feature_columns]
    y = df['asthma_risk']
    
    # Encode target labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    return X, y_encoded, le, feature_columns

def augment_data(X, y, n_augment=1000):
    """Augment the dataset with synthetic data"""
    # Combine features and target
    df = pd.DataFrame(X)
    df['target'] = y
    
    # Generate synthetic data
    augmented_data = []
    for _ in range(n_augment):
        # Randomly select a row
        sample_idx = np.random.randint(0, len(df))
        sample = df.iloc[sample_idx].copy()
        
        # Add small noise to features
        noise_factor = 0.1
        for col in df.columns[:-1]:  # Exclude target column
            noise = np.random.normal(0, noise_factor * abs(sample[col]))
            sample[col] += noise
            
        # Ensure realistic bounds
        sample['pm25'] = max(0, sample['pm25'])
        sample['pm10'] = max(0, sample['pm10'])
        sample['humidity'] = max(0, min(100, sample['humidity']))
        sample['medication_adherence'] = max(0, min(1, sample['medication_adherence']))
        
        augmented_data.append(sample)
    
    # Combine original and augmented data
    augmented_df = pd.DataFrame(augmented_data)
    combined_df = pd.concat([df, augmented_df], ignore_index=True)
    
    X_combined = combined_df.drop('target', axis=1)
    y_combined = combined_df['target']
    
    print(f"Data augmented: {len(df)} -> {len(combined_df)} samples")
    return X_combined, y_combined

def train_multiple_models(X_train, y_train, X_test, y_test):
    """Train multiple models and compare their performance"""
    # Define models to train
    models = {
        'Random Forest': RandomForestClassifier(random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'SVM': SVC(random_state=42, probability=True)
    }
    
    # Define hyperparameter grids for tuning
    param_grids = {
        'Random Forest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5]
        },
        'Logistic Regression': {
            'C': [0.1, 1, 10],
            'solver': ['liblinear', 'lbfgs']
        },
        'Gradient Boosting': {
            'n_estimators': [50, 100, 200],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 5, 7]
        },
        'SVM': {
            'C': [0.1, 1, 10],
            'kernel': ['rbf', 'linear'],
            'gamma': ['scale', 'auto']
        }
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Create pipeline with scaling
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', model)
        ])
        
        # Perform grid search for hyperparameter tuning
        try:
            grid_search = GridSearchCV(
                pipeline, 
                param_grids.get(name, {}), 
                cv=3, 
                scoring='accuracy',
                n_jobs=-1,
                verbose=0
            )
            grid_search.fit(X_train, y_train)
            
            # Get best model
            best_model = grid_search.best_estimator_
            
            # Evaluate on test set
            y_pred = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Cross-validation score
            cv_scores = cross_val_score(best_model, X_train, y_train, cv=5)
            
            results[name] = {
                'model': best_model,
                'accuracy': accuracy,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'best_params': grid_search.best_params_,
                'predictions': y_pred
            }
            
            print(f"  Test Accuracy: {accuracy:.4f}")
            print(f"  CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
            
        except Exception as e:
            print(f"  Error training {name}: {str(e)}")
            continue
    
    return results

def evaluate_models(results, y_test, le):
    """Evaluate and compare all trained models"""
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)
    
    # Sort models by accuracy
    sorted_models = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)
    
    for name, result in sorted_models:
        print(f"\n{name}:")
        print(f"  Test Accuracy: {result['accuracy']:.4f}")
        print(f"  CV Score: {result['cv_mean']:.4f} (+/- {result['cv_std'] * 2:.4f})")
        print(f"  Best Parameters: {result['best_params']}")
        
        # Detailed classification report
        print("  Classification Report:")
        print(classification_report(y_test, result['predictions'], target_names=le.classes_))
    
    # Select best model
    best_model_name = sorted_models[0][0]
    best_model = results[best_model_name]['model']
    
    print(f"\nBest Model: {best_model_name}")
    print(f"Best Accuracy: {results[best_model_name]['accuracy']:.4f}")
    
    return best_model_name, best_model

def save_model(model, le, model_name, feature_columns):
    """Save the trained model and related components"""
    model_dir = os.path.join('asthmashield_app', 'ml_model')
    
    # Save the model
    model_path = os.path.join(model_dir, f'{model_name.lower().replace(" ", "_")}_model.pkl')
    joblib.dump(model, model_path)
    
    # Save the label encoder
    encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
    joblib.dump(le, encoder_path)
    
    # Save feature columns for reference
    feature_path = os.path.join(model_dir, 'feature_columns.pkl')
    joblib.dump(feature_columns, feature_path)
    
    print(f"\nModel saved to {model_path}")
    print(f"Label encoder saved to {encoder_path}")
    print(f"Feature columns saved to {feature_path}")

def generate_risk_insights(X, y, le, feature_columns):
    """Generate insights about risk factors"""
    print("\n" + "="*60)
    print("RISK FACTOR INSIGHTS")
    print("="*60)
    
    # Convert encoded labels back to original
    y_labels = le.inverse_transform(y)
    
    # Create DataFrame for analysis
    df = pd.DataFrame(X, columns=feature_columns)
    df['risk_level'] = y_labels
    
    # Analyze feature distributions by risk level
    for risk in le.classes_:
        risk_data = df[df['risk_level'] == risk]
        print(f"\n{risk} Risk Level Statistics:")
        print(risk_data[feature_columns].describe().round(2))
    
    # Feature importance (for tree-based models)
    # This would be more detailed in a real implementation

def validate_xai_compatibility(model):
    """Validate that the model is compatible with XAI explanations"""
    try:
        # Check if model has predict_proba method (required for XAI)
        if not hasattr(model.named_steps['classifier'], 'predict_proba'):
            print("Warning: Model does not have predict_proba method, XAI explanations may be limited")
            return False
        
        # Check if model supports feature importance (for SHAP)
        if hasattr(model.named_steps['classifier'], 'feature_importances_'):
            print("Model supports SHAP TreeExplainer")
        else:
            print("Model will use SHAP KernelExplainer (slower but works with any model)")
        
        print("Model is compatible with XAI explanations")
        return True
    except Exception as e:
        print(f"XAI compatibility check failed: {str(e)}")
        return False

def train_model(model_type='best', augment_data_flag=True):
    """Train the asthma risk prediction model with enhanced features"""
    print("Loading and preprocessing data...")
    X, y_encoded, le, feature_columns = load_and_preprocess_data()
    
    # Augment data if requested
    if augment_data_flag:
        print("\nAugmenting data...")
        X, y_encoded = augment_data(X, y_encoded, n_augment=1000)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"\nTraining set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train multiple models
    print("\nTraining multiple models...")
    results = train_multiple_models(X_train, y_train, X_test, y_test)
    
    if not results:
        print("No models were successfully trained!")
        return None, None
    
    # Evaluate models
    best_model_name, best_model = evaluate_models(results, y_test, le)
    
    # Validate XAI compatibility
    print("\n" + "="*60)
    print("XAI COMPATIBILITY CHECK")
    print("="*60)
    validate_xai_compatibility(best_model)
    
    # Generate insights
    generate_risk_insights(X, y_encoded, le, feature_columns)
    
    # Save the best model
    save_model(best_model, le, best_model_name, feature_columns)
    
    return best_model, le

def main():
    parser = argparse.ArgumentParser(description='Train asthma risk prediction model with enhanced accuracy')
    parser.add_argument('--model', choices=['best', 'random_forest', 'logistic_regression', 'gradient_boosting', 'svm'], 
                       default='best', help='Model type to train')
    parser.add_argument('--no-augment', action='store_true', 
                       help='Disable data augmentation')
    
    args = parser.parse_args()
    train_model(args.model, not args.no_augment)

if __name__ == "__main__":
    main()