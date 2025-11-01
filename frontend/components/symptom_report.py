"""
Symptom reporting component for the AsthmaShield frontend
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time

def render_symptom_report_form():
    """Render the symptom reporting form"""
    st.subheader("🩺 Report Symptoms")
    st.info("Help improve air quality predictions by reporting your symptoms. All data is anonymous and used for research purposes only.")
    
    # Symptom checkboxes
    st.write("Select your current symptoms:")
    col1, col2 = st.columns(2)
    
    with col1:
        wheezing = st.checkbox("Wheezing", key="wheezing")
        shortness_of_breath = st.checkbox("Shortness of breath", key="shortness_of_breath")
        chest_tightness = st.checkbox("Chest tightness", key="chest_tightness")
    
    with col2:
        coughing = st.checkbox("Coughing", key="coughing")
        difficulty_sleeping = st.checkbox("Difficulty sleeping", key="difficulty_sleeping")
    
    # Severity slider
    severity = st.select_slider(
        "How severe are your symptoms?",
        options=["Mild", "Moderate", "Severe"],
        value="Mild"
    )
    
    # Location (optional)
    st.write("Location (optional):")
    use_current_location = st.checkbox("Use my current location")
    
    lat, lon = None, None
    if use_current_location:
        # In a real implementation, you would get the actual location
        # For now, we'll use default values
        lat, lon = 18.5204, 73.8567  # Pune coordinates
        st.info(f"Using location: {lat}, {lon}")
    else:
        # Manual location input
        city = st.text_input("City", "Pune")
        # In a real implementation, you would geocode the city to get coordinates
    
    # Submit button
    if st.button("Submit Symptom Report"):
        if not any([wheezing, shortness_of_breath, chest_tightness, coughing, difficulty_sleeping]):
            st.warning("Please select at least one symptom.")
            return
        
        # Prepare symptom data
        symptoms = {
            "wheezing": wheezing,
            "shortness_of_breath": shortness_of_breath,
            "chest_tightness": chest_tightness,
            "coughing": coughing,
            "difficulty_sleeping": difficulty_sleeping
        }
        
        location = {}
        if lat and lon:
            location = {
                "latitude": lat,
                "longitude": lon
            }
        
        # Prepare report data
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "user_id": "anonymous",  # In a real app, this would be the actual user ID
            "symptoms": symptoms,
            "location": location,
            "severity": severity
        }
        
        # Send to backend
        try:
            backend_url = "http://localhost:8000/api/symptom-report/"
            response = requests.post(
                backend_url,
                json=report_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                st.success("Symptom report submitted successfully! Thank you for contributing to asthma research.")
                time.sleep(2)
                st.experimental_rerun()
            else:
                st.error(f"Failed to submit report: {response.status_code}")
        except Exception as e:
            st.error(f"Error submitting report: {str(e)}")

def render_symptom_trends():
    """Render symptom trends visualization"""
    st.subheader("📊 Community Symptom Trends")
    
    # In a real implementation, you would fetch this data from the backend
    # For now, we'll show a placeholder
    st.info("Community symptom data will appear here once enough reports are collected.")
    
    # Example visualization (placeholder)
    st.write("Recent symptom reports in your area:")
    st.progress(0.4)  # Placeholder for actual data
    st.caption("40% of reports indicate mild symptoms, 35% moderate, 25% severe")

# For testing purposes
if __name__ == "__main__":
    # This would be called from the main app.py
    pass