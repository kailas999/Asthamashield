import streamlit as st
import requests
import os
from dotenv import load_dotenv
from components.map_component import create_risk_map, add_city_marker
from components.weather_card import display_weather_card, display_risk_card
from components.symptom_report import render_symptom_report_form, render_symptom_trends
from streamlit_folium import st_folium

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AsthmaShield - AI Asthma Risk Predictor",
    page_icon="🌬️",
    layout="wide"
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-header'>🌬️ AsthmaShield – AI Asthma Risk Predictor</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("About AsthmaShield")
st.sidebar.info("""
AsthmaShield is an AI-powered platform that predicts asthma risk levels based on real-time environmental data including air quality, weather conditions, and pollen counts.
""")

st.sidebar.header("How it works")
st.sidebar.info("""
1. Enter your city name
2. Our system fetches real-time weather and air quality data
3. AI model predicts asthma risk level
4. XAI explanations help understand predictions
5. Receive personalized health advice
""")

# Expandable sections
with st.expander("💊 Medication Reminder", expanded=False):
    st.subheader("Set Medication Reminders")
    st.info("Never miss your medication with personalized reminders.")
    
    medication_name = st.text_input("Medication Name", "Inhaler")
    dosage_time = st.time_input("Dosage Time")
    
    user_email = st.text_input("Email for reminders", "")
    user_phone = st.text_input("Phone for SMS reminders", "")
    
    if st.button("Set Reminder"):
        if user_email or user_phone:
            try:
                backend_url = "http://localhost:8000/api/medication-reminder/"
                reminder_data = {
                    "name": "User",
                    "email": user_email if user_email else "",
                    "phone": user_phone if user_phone else "",
                    "medication_name": medication_name,
                    "dosage_time": str(dosage_time)
                }
                response = requests.post(
                    backend_url,
                    json=reminder_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    st.success("Medication reminder set successfully!")
                else:
                    st.error(f"Failed to set reminder: {response.status_code}")
            except Exception as e:
                st.error(f"Error setting reminder: {str(e)}")
        else:
            st.warning("Please provide an email or phone number for reminders.")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📍 Location & Patient Info")
    city = st.text_input("Enter your city:", "Pune")
    
    # Patient information inputs
    st.subheader("👤 Patient Information")
    patient_age = st.number_input("Age", min_value=5, max_value=100, value=35)
    patient_history_severe_attacks = st.number_input("Severe attacks in past year", min_value=0, max_value=20, value=1)
    medication_adherence = st.slider("Medication adherence (%)", min_value=0, max_value=100, value=80) / 100.0
    
    # Contact information for alerts
    st.subheader("📢 Notification Preferences")
    user_email = st.text_input("Email for alerts", "")
    user_phone = st.text_input("Phone for SMS alerts", "")
    
    if st.button("Check Risk", key="check_risk"):
        if city:
            with st.spinner("Analyzing environmental and patient data..."):
                try:
                    # Call backend API
                    backend_url = "http://localhost:8000/api/predict/"
                    params = {
                        'city': city,
                        'patient_age': patient_age,
                        'patient_history_severe_attacks': patient_history_severe_attacks,
                        'medication_adherence': medication_adherence,
                        'email': user_email,
                        'phone': user_phone
                    }
                    response = requests.get(backend_url, params=params)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Display data cards
                        st.subheader("📊 Live Environmental Data")
                        
                        col_data1, col_data2 = st.columns(2)
                        with col_data1:
                            display_weather_card("🌡️ Temperature", f"{data['temperature']:.1f}", "°C", "🌡️", "#2196f3")
                            display_weather_card("💨 PM2.5", f"{data['pm25']:.1f}", "μg/m³", "💨", "#f44336")
                            display_weather_card("🌪️ Wind Speed", f"{data['wind_speed']:.1f}", "m/s", "🌪️", "#ff9800")
                        
                        with col_data2:
                            display_weather_card("💧 Humidity", f"{data['humidity']:.1f}", "%", "💧", "#4caf50")
                            display_weather_card("🏭 PM10", f"{data['pm10']:.1f}", "μg/m³", "🏭", "#ff5722")
                            display_weather_card("📏 Pressure", f"{data['pressure']:.0f}", "hPa", "📏", "#9c27b0")
                        
                        # Display patient information
                        st.subheader("👤 Patient Information")
                        col_patient1, col_patient2, col_patient3 = st.columns(3)
                        with col_patient1:
                            display_weather_card("🎂 Age", f"{data['patient_age']}", "years", "🎂", "#3f51b5")
                        with col_patient2:
                            display_weather_card("⚠️ Severe Attacks", f"{data['patient_history_severe_attacks']}", "", "⚠️", "#f44336")
                        with col_patient3:
                            display_weather_card("💊 Adherence", f"{data['medication_adherence']*100:.0f}", "%", "💊", "#4caf50")
                        
                        # Display risk level
                        st.subheader("⚠️ Asthma Risk Level")
                        display_risk_card(data['asthma_risk'])
                        
                        # Display confidence and probabilities
                        if data.get('confidence'):
                            st.metric("Prediction Confidence", f"{data['confidence']*100:.1f}%")
                        
                        # Display XAI explanations
                        if data.get('xai_explanations'):
                            st.subheader("🔍 Why This Prediction?")
                            xai_exp = data['xai_explanations']
                            
                            # Show top contributing factors
                            if 'lime' in xai_exp and 'feature_weights' in xai_exp['lime']:
                                st.write("**Top contributing factors (LIME):**")
                                feature_weights = xai_exp['lime']['feature_weights']
                                sorted_features = sorted(feature_weights.items(), key=lambda x: abs(x[1]), reverse=True)
                                
                                for feature, weight in sorted_features[:5]:
                                    weight_pct = abs(weight) * 100
                                    indicator = "⬆️" if weight > 0 else "⬇️"
                                    st.write(f"{indicator} {feature}: {weight_pct:.1f}% impact")
                            
                            # Show SHAP values if available
                            if 'shap' in xai_exp and 'feature_importance' in xai_exp['shap']:
                                st.write("**Feature importance (SHAP):**")
                                shap_importance = xai_exp['shap']['feature_importance']
                                sorted_shap = sorted(shap_importance.items(), key=lambda x: abs(x[1]), reverse=True)
                                
                                for feature, importance in sorted_shap[:5]:
                                    st.write(f"- {feature}: {importance:.3f}")
                        
                        # Display AI advice
                        st.subheader("🤖 AI Health Advice")
                        st.info(data['advice'])
                        
                        # Display local symptom reports
                        if data.get('local_symptom_reports'):
                            st.subheader("🩺 Community Reports")
                            reports = data['local_symptom_reports']
                            st.write(f"Recent reports in your area: {len(reports)}")
                            # In a real implementation, you would visualize these reports
                    else:
                        st.error(f"Error fetching data: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a city name")

with col2:
    st.header("🗺️ Risk Map")
    
    # Create a simple map centered on India
    m = create_risk_map(20.5937, 78.9629, 5)
    
    # Add a marker for the selected city (Pune as default)
    add_city_marker(m, 18.5204, 73.8567, "Pune", "High", {
        'pm25': 92,
        'temperature': 31
    })
    
    # Display the map using streamlit-folium
    st_folium(m, width=700, height=500)
    
    # Render symptom trends
    render_symptom_trends()

# Symptom reporting section
st.header("🩺 Community Symptom Reporting")
render_symptom_report_form()

# Additional information
st.header("📈 About Our Data Sources")
col_sources1, col_sources2, col_sources3 = st.columns(3)

with col_sources1:
    st.subheader("🌤️ Weather Data")
    st.info("OpenWeatherMap API provides real-time weather information including temperature, humidity, and atmospheric pressure.")

with col_sources2:
    st.subheader("🏭 Air Quality")
    st.info("OpenWeather Air Pollution API delivers current air quality data including PM2.5, PM10, and other pollutant levels.")

with col_sources3:
    st.subheader("🧠 AI Insights")
    st.info("Our ML models analyze environmental and patient data to provide personalized health recommendations and preventive advice. XAI explanations help understand model predictions.")