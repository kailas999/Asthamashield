"""
Script to validate the asthma dataset quality and consistency
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import os

def load_dataset():
    """Load the asthma dataset"""
    try:
        data_path = os.path.join('datasets', 'asthma_data.csv')
        df = pd.read_csv(data_path)
        print(f"Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except FileNotFoundError:
        print("Error: asthma_data.csv not found in datasets directory")
        return None

def check_data_quality(df):
    """Perform comprehensive data quality checks"""
    print("\n" + "="*50)
    print("DATA QUALITY REPORT")
    print("="*50)
    
    # Basic info
    print(f"Dataset shape: {df.shape}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Missing values
    missing_data = df.isnull().sum()
    if missing_data.sum() > 0:
        print("\nMissing values:")
        for col, count in missing_data[missing_data > 0].items():
            print(f"  {col}: {count} ({count/len(df)*100:.2f}%)")
    else:
        print("\n✓ No missing values found")
    
    # Duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"\n⚠ {duplicates} duplicate rows found")
    else:
        print("\n✓ No duplicate rows found")
    
    # Data types
    print("\nData types:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")
    
    return missing_data, duplicates

def validate_value_ranges(df):
    """Validate that values are within expected ranges"""
    print("\n" + "="*50)
    print("VALUE RANGE VALIDATION")
    print("="*50)
    
    # Define expected ranges
    expected_ranges = {
        'pm25': (0, 1000),
        'pm10': (0, 1000),
        'temperature': (-50, 60),
        'humidity': (0, 100),
        'pollen_level': (0, 100),
        'wind_speed': (0, 50),
        'pressure': (900, 1100),
        'patient_age': (0, 120),
        'patient_history_severe_attacks': (0, 50),
        'medication_adherence': (0, 1)
    }
    
    issues_found = []
    
    for col, (min_val, max_val) in expected_ranges.items():
        if col in df.columns:
            out_of_range = df[(df[col] < min_val) | (df[col] > max_val)]
            if len(out_of_range) > 0:
                issues_found.append((col, len(out_of_range)))
                print(f"⚠ {col}: {len(out_of_range)} values out of range [{min_val}, {max_val}]")
                print(f"  Min: {df[col].min()}, Max: {df[col].max()}")
            else:
                print(f"✓ {col}: All values within range [{min_val}, {max_val}]")
    
    if not issues_found:
        print("✓ All values are within expected ranges")
    
    return issues_found

def validate_categorical_data(df):
    """Validate categorical data (risk levels)"""
    print("\n" + "="*50)
    print("CATEGORICAL DATA VALIDATION")
    print("="*50)
    
    if 'asthma_risk' in df.columns:
        valid_risk_levels = ['Low', 'Moderate', 'High']
        invalid_risks = df[~df['asthma_risk'].isin(valid_risk_levels)]
        
        if len(invalid_risks) > 0:
            print(f"⚠ Invalid risk levels found: {invalid_risks['asthma_risk'].unique()}")
        else:
            print("✓ All risk levels are valid")
            print(f"Risk distribution:")
            print(df['asthma_risk'].value_counts().sort_index())
    
    return df['asthma_risk'].value_counts() if 'asthma_risk' in df.columns else None

def analyze_feature_correlations(df):
    """Analyze correlations between features and target"""
    print("\n" + "="*50)
    print("FEATURE CORRELATION ANALYSIS")
    print("="*50)
    
    # Encode categorical target for correlation analysis
    df_encoded = df.copy()
    if 'asthma_risk' in df_encoded.columns:
        le = LabelEncoder()
        df_encoded['asthma_risk_encoded'] = le.fit_transform(df_encoded['asthma_risk'])
    
    # Calculate correlations
    numeric_columns = df_encoded.select_dtypes(include=[np.number]).columns
    correlation_matrix = df_encoded[numeric_columns].corr()
    
    # Show correlations with target
    if 'asthma_risk_encoded' in correlation_matrix.columns:
        target_corr = correlation_matrix['asthma_risk_encoded'].abs().sort_values(ascending=False)
        print("Feature correlations with asthma risk (absolute values):")
        for feature, corr in target_corr.items():
            if feature != 'asthma_risk_encoded':
                print(f"  {feature}: {corr:.3f}")
    
    return correlation_matrix

def generate_summary_statistics(df):
    """Generate comprehensive summary statistics"""
    print("\n" + "="*50)
    print("SUMMARY STATISTICS")
    print("="*50)
    
    # Overall statistics
    print("Dataset Overview:")
    print(df.describe())
    
    # Risk level statistics
    if 'asthma_risk' in df.columns:
        print("\nStatistics by Risk Level:")
        for risk_level in df['asthma_risk'].unique():
            print(f"\n{risk_level} Risk:")
            risk_data = df[df['asthma_risk'] == risk_level]
            print(risk_data.describe().round(2))

def create_visualizations(df):
    """Create visualizations to understand the data"""
    print("\n" + "="*50)
    print("DATA VISUALIZATION")
    print("="*50)
    
    # Set up the plotting style
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Asthma Dataset Analysis', fontsize=16)
    
    # Risk level distribution
    axes[0, 0].pie(df['asthma_risk'].value_counts(), labels=df['asthma_risk'].value_counts().index, autopct='%1.1f%%')
    axes[0, 0].set_title('Risk Level Distribution')
    
    # PM2.5 distribution by risk level
    df.boxplot(column='pm25', by='asthma_risk', ax=axes[0, 1])
    axes[0, 1].set_title('PM2.5 Distribution by Risk Level')
    axes[0, 1].set_xlabel('Risk Level')
    axes[0, 1].set_ylabel('PM2.5 (μg/m³)')
    
    # Temperature vs Humidity scatter plot
    scatter = axes[1, 0].scatter(df['temperature'], df['humidity'], c=pd.factorize(df['asthma_risk'])[0], alpha=0.6)
    axes[1, 0].set_xlabel('Temperature (°C)')
    axes[1, 0].set_ylabel('Humidity (%)')
    axes[1, 0].set_title('Temperature vs Humidity by Risk Level')
    
    # Medication adherence distribution
    df['medication_adherence'].hist(bins=20, ax=axes[1, 1], alpha=0.7)
    axes[1, 1].set_xlabel('Medication Adherence')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Medication Adherence Distribution')
    
    plt.tight_layout()
    plt.savefig(os.path.join('datasets', 'data_analysis.png'), dpi=300, bbox_inches='tight')
    print("Visualization saved as 'data_analysis.png'")
    
    # Show correlation heatmap
    plt.figure(figsize=(12, 10))
    numeric_df = df.select_dtypes(include=[np.number])
    if 'asthma_risk' in df.columns:
        # Encode asthma_risk for correlation
        df_temp = df.copy()
        le = LabelEncoder()
        df_temp['asthma_risk_encoded'] = le.fit_transform(df_temp['asthma_risk'])
        numeric_df = df_temp.select_dtypes(include=[np.number])
    
    correlation_matrix = numeric_df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join('datasets', 'correlation_heatmap.png'), dpi=300, bbox_inches='tight')
    print("Correlation heatmap saved as 'correlation_heatmap.png'")

def validate_dataset_completeness(df):
    """Validate that the dataset is complete and suitable for training"""
    print("\n" + "="*50)
    print("DATASET COMPLETENESS VALIDATION")
    print("="*50)
    
    required_columns = [
        'pm25', 'pm10', 'temperature', 'humidity', 'pollen_level',
        'wind_speed', 'pressure', 'patient_age',
        'patient_history_severe_attacks', 'medication_adherence', 'asthma_risk'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"⚠ Missing required columns: {missing_columns}")
        return False
    else:
        print("✓ All required columns present")
    
    # Check for sufficient samples per class
    if 'asthma_risk' in df.columns:
        risk_counts = df['asthma_risk'].value_counts()
        min_samples = 50  # Minimum samples per class for good training
        insufficient_classes = risk_counts[risk_counts < min_samples]
        
        if len(insufficient_classes) > 0:
            print(f"⚠ Classes with insufficient samples (<{min_samples}):")
            for risk, count in insufficient_classes.items():
                print(f"  {risk}: {count} samples")
        else:
            print("✓ Sufficient samples for all risk classes")
    
    # Check for data balance
    if 'asthma_risk' in df.columns:
        risk_counts = df['asthma_risk'].value_counts()
        max_count = risk_counts.max()
        min_count = risk_counts.min()
        balance_ratio = min_count / max_count
        
        if balance_ratio < 0.5:
            print(f"⚠ Dataset may be imbalanced (balance ratio: {balance_ratio:.2f})")
        else:
            print(f"✓ Dataset balance is acceptable (balance ratio: {balance_ratio:.2f})")
    
    print("\nDataset validation completed!")
    return True

def main():
    """Main validation function"""
    # Load dataset
    df = load_dataset()
    if df is None:
        return
    
    # Perform all validations
    missing_data, duplicates = check_data_quality(df)
    range_issues = validate_value_ranges(df)
    risk_distribution = validate_categorical_data(df)
    correlation_matrix = analyze_feature_correlations(df)
    generate_summary_statistics(df)
    
    # Try to create visualizations (may fail if matplotlib backend issues)
    try:
        create_visualizations(df)
    except Exception as e:
        print(f"Warning: Could not create visualizations: {e}")
    
    # Validate completeness
    is_complete = validate_dataset_completeness(df)
    
    # Summary
    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50)
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Missing values: {missing_data.sum()}")
    print(f"Duplicate rows: {duplicates}")
    print(f"Range issues: {len(range_issues)}")
    if risk_distribution is not None:
        print(f"Risk classes: {len(risk_distribution)}")
        print(f"Risk distribution: {dict(risk_distribution)}")

if __name__ == "__main__":
    main()