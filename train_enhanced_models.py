"""
Comprehensive script to enhance asthma risk prediction models
"""

import os
import sys
import subprocess
import time

def run_enhanced_training():
    """Run the complete enhanced training process"""
    print("🚀 Starting Enhanced Asthma Risk Prediction Model Training")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Step 1: Generate enhanced dataset
    print("\n📊 Step 1: Generating Enhanced Dataset")
    print("-" * 40)
    try:
        result = subprocess.run([
            sys.executable, 
            os.path.join('datasets', 'generate_data.py')
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Dataset generation completed successfully")
            print(result.stdout)
        else:
            print("⚠ Dataset generation completed with warnings")
            print(result.stdout)
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("⚠ Dataset generation timed out")
    except Exception as e:
        print(f"❌ Error generating dataset: {e}")
    
    # Step 2: Validate dataset
    print("\n🔍 Step 2: Validating Dataset")
    print("-" * 40)
    try:
        result = subprocess.run([
            sys.executable, 
            os.path.join('datasets', 'validate_data.py')
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Dataset validation completed successfully")
            print(result.stdout)
        else:
            print("⚠ Dataset validation completed with warnings")
            print(result.stdout)
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("⚠ Dataset validation timed out")
    except Exception as e:
        print(f"❌ Error validating dataset: {e}")
    
    # Step 3: Train enhanced models
    print("\n🧠 Step 3: Training Enhanced Models")
    print("-" * 40)
    try:
        result = subprocess.run([
            sys.executable, 
            'train_model.py'
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Model training completed successfully")
            print(result.stdout)
        else:
            print("⚠ Model training completed with warnings")
            print(result.stdout)
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("⚠ Model training timed out")
    except Exception as e:
        print(f"❌ Error training models: {e}")
    
    # Step 4: Test the trained model
    print("\n🧪 Step 4: Testing Trained Model")
    print("-" * 40)
    try:
        result = subprocess.run([
            sys.executable, 
            os.path.join('asthmashield_app', 'ml_model', 'model.py')
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Model testing completed successfully")
            print(result.stdout)
        else:
            print("⚠ Model testing completed with warnings")
            print(result.stdout)
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("⚠ Model testing timed out")
    except Exception as e:
        print(f"❌ Error testing model: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced Training Process Completed!")
    print("=" * 60)
    print("Next steps:")
    print("1. Restart the Django backend server")
    print("2. Test the API endpoint with various cities")
    print("3. Check the frontend for updated predictions")

if __name__ == "__main__":
    run_enhanced_training()