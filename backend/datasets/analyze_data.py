"""
Data analysis script for AsthmaShield dataset
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

def analyze_dataset():
    """Analyze the asthma dataset"""
    # Load the dataset
    df = pd.read_csv('asthma_data.csv')
    
    # Display basic information
    print("Dataset Info:")
    print(df.info())
    
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nDataset Statistics:")
    print(df.describe())
    
    # Count of each risk level
    print("\nRisk Level Distribution:")
    print(df['asthma_risk'].value_counts())
    
    # Correlation matrix
    print("\nCorrelation with Asthma Risk:")
    # Encode categorical variables for correlation analysis
    df_encoded = df.copy()
    le = LabelEncoder()
    df_encoded['asthma_risk'] = le.fit_transform(df_encoded['asthma_risk'])
    
    correlation = df_encoded.corr()
    asthma_risk_corr = correlation['asthma_risk']
    print(asthma_risk_corr)
    
    # Plot some visualizations
    plt.figure(figsize=(15, 12))
    
    # Distribution of risk levels
    plt.subplot(3, 3, 1)
    df['asthma_risk'].value_counts().plot(kind='bar')
    plt.title('Distribution of Asthma Risk Levels')
    plt.xlabel('Risk Level')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    
    # Scatter plot of PM2.5 vs PM10
    plt.subplot(3, 3, 2)
    sns.scatterplot(data=df, x='pm25', y='pm10', hue='asthma_risk')
    plt.title('PM2.5 vs PM10 by Risk Level')
    
    # Temperature distribution by risk level
    plt.subplot(3, 3, 3)
    sns.boxplot(data=df, x='asthma_risk', y='temperature')
    plt.title('Temperature by Risk Level')
    plt.xticks(rotation=0)
    
    # Humidity distribution by risk level
    plt.subplot(3, 3, 4)
    sns.boxplot(data=df, x='asthma_risk', y='humidity')
    plt.title('Humidity by Risk Level')
    plt.xticks(rotation=0)
    
    # Patient age distribution by risk level
    plt.subplot(3, 3, 5)
    sns.boxplot(data=df, x='asthma_risk', y='patient_age')
    plt.title('Patient Age by Risk Level')
    plt.xticks(rotation=0)
    
    # Medication adherence by risk level
    plt.subplot(3, 3, 6)
    sns.boxplot(data=df, x='asthma_risk', y='medication_adherence')
    plt.title('Medication Adherence by Risk Level')
    plt.xticks(rotation=0)
    
    # History of severe attacks by risk level
    plt.subplot(3, 3, 7)
    sns.boxplot(data=df, x='asthma_risk', y='patient_history_severe_attacks')
    plt.title('History of Severe Attacks by Risk Level')
    plt.xticks(rotation=0)
    
    # Pollen level by risk level
    plt.subplot(3, 3, 8)
    sns.boxplot(data=df, x='asthma_risk', y='pollen_level')
    plt.title('Pollen Level by Risk Level')
    plt.xticks(rotation=0)
    
    # Wind speed by risk level
    plt.subplot(3, 3, 9)
    sns.boxplot(data=df, x='asthma_risk', y='wind_speed')
    plt.title('Wind Speed by Risk Level')
    plt.xticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nAnalysis complete. Plot saved as 'dataset_analysis.png'")

if __name__ == "__main__":
    analyze_dataset()