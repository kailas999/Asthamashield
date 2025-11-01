"""
Complete workflow demonstration script for AsthmaShield
"""

import os
import subprocess
import sys

def run_workflow():
    """Demonstrate the complete AsthmaShield workflow"""
    print("AsthmaShield Complete Workflow Demonstration")
    print("=" * 50)
    
    # Step 1: Generate additional sample data
    print("Step 1: Generating additional sample data...")
    try:
        subprocess.run([sys.executable, "datasets/generate_data.py"], check=True, cwd="backend")
        print("✓ Sample data generated successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to generate sample data")
        return
    
    # Step 2: Validate the dataset
    print("\nStep 2: Validating dataset...")
    try:
        subprocess.run([sys.executable, "datasets/validate_data.py"], check=True, cwd="backend")
        print("✓ Dataset validation completed")
    except subprocess.CalledProcessError:
        print("✗ Dataset validation failed")
        return
    
    # Step 3: Train ML models
    print("\nStep 3: Training ML models...")
    try:
        # Train Random Forest (default)
        subprocess.run([sys.executable, "train_model.py"], check=True, cwd="backend")
        print("✓ Random Forest model trained successfully")
        
        # Train Logistic Regression
        subprocess.run([sys.executable, "train_model.py", "--model", "logistic_regression"], 
                      check=True, cwd="backend")
        print("✓ Logistic Regression model trained successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to train ML models")
        return
    
    # Step 4: Generate model report
    print("\nStep 4: Generating model comparison report...")
    try:
        subprocess.run([sys.executable, "generate_model_report.py"], check=True, cwd="backend")
        print("✓ Model comparison report generated")
    except subprocess.CalledProcessError:
        print("✗ Failed to generate model report")
        return
    
    # Step 5: Demonstrate model usage
    print("\nStep 5: Demonstrating model usage...")
    try:
        subprocess.run([sys.executable, "demo_models.py"], check=True, cwd="backend")
        print("✓ Model usage demonstration completed")
    except subprocess.CalledProcessError:
        print("✗ Model usage demonstration failed")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Complete workflow demonstration finished successfully!")
    print("\nNext steps:")
    print("1. Start the Django backend: python manage.py runserver")
    print("2. Start the Streamlit frontend: streamlit run app.py")
    print("3. Access the application at http://localhost:8501")

if __name__ == "__main__":
    run_workflow()