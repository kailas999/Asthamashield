"""
Setup script for AsthmaShield project
"""

from setuptools import setup, find_packages

setup(
    name="asthmashield",
    version="1.0.0",
    description="AI-powered Asthma Risk & Environmental Health Dashboard",
    author="AsthmaShield Team",
    packages=find_packages(),
    install_requires=[
        # Backend requirements
        "Django>=4.2.7",
        "djangorestframework>=3.14.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "numpy>=1.24.3",
        "pandas>=2.0.3",
        "scikit-learn>=1.3.0",
        "joblib>=1.3.2",
        "google-generativeai>=0.3.1",
        
        # Frontend requirements
        "streamlit>=1.28.0",
        "folium>=0.14.0",
        "streamlit-folium>=0.15.0",
    ],
    python_requires=">=3.8",
)