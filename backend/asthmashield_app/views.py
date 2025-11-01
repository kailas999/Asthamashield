from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import requests
import os
from dotenv import load_dotenv
import json
from .ml_model.model import predict_asthma_risk, get_feature_importance
from .notifications import send_asthma_alert, send_medication_reminder
from .data_collection import save_symptom_report, get_local_symptom_reports

# Load environment variables
load_dotenv()

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
    def get(self, request):
        city = request.GET.get('city', 'Pune')
        
        # Get additional parameters (with defaults)
        patient_age = int(request.GET.get('patient_age', 35))
        patient_history_severe_attacks = int(request.GET.get('patient_history_severe_attacks', 1))
        medication_adherence = float(request.GET.get('medication_adherence', 0.8))
        
        # Get user contact information for notifications
        user_email = request.GET.get('email', '')
        user_phone = request.GET.get('phone', '')
        
        # Get weather and AQI data
        try:
            # OpenWeather API calls
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('OPENWEATHER_API')}"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()
            
            # Check if API call was successful
            if weather_data.get('cod') != 200:
                return JsonResponse({'error': f"Weather API error: {weather_data.get('message', 'Unknown error')}"}, status=400)
            
            # Extract coordinates for AQI API
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            
            # AQI API call
            aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={os.getenv('OPENWEATHER_API')}"
            aqi_response = requests.get(aqi_url)
            aqi_data = aqi_response.json()
            
            # Check if AQI API call was successful
            if not aqi_data.get('list'):
                return JsonResponse({'error': 'AQI data not available'}, status=400)
            
            # Extract environmental data
            temperature = weather_data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
            humidity = weather_data['main']['humidity']
            pressure = weather_data['main']['pressure']
            wind_speed = weather_data['wind']['speed'] if 'wind' in weather_data else 0
            pm25 = aqi_data['list'][0]['components']['pm2_5']
            pm10 = aqi_data['list'][0]['components']['pm10']
            
            # Use default values for missing data
            pollen_level = 50  # Default pollen level
            
            # Use ML model for prediction with confidence and XAI explanations
            prediction_result = predict_asthma_risk(
                pm25=pm25, pm10=pm10, temperature=temperature, humidity=humidity, 
                pollen_level=pollen_level, wind_speed=wind_speed, pressure=pressure,
                patient_age=patient_age, 
                patient_history_severe_attacks=patient_history_severe_attacks, 
                medication_adherence=medication_adherence,
                include_xai=True
            )
            
            asthma_risk = prediction_result['risk_level']
            confidence = prediction_result['confidence']
            probabilities = prediction_result['probabilities']
            xai_explanations = prediction_result.get('xai_explanations', {})
            
            # Send alert if risk is high
            if asthma_risk == 'High' and (user_email or user_phone):
                user_info = {
                    'name': 'User',
                    'city': city,
                    'email': user_email,
                    'phone': user_phone,
                    'latitude': lat,
                    'longitude': lon
                }
                
                environmental_data = {
                    'pm25': pm25,
                    'pm10': pm10,
                    'temperature': temperature,
                    'humidity': humidity,
                    'pollen_level': pollen_level,
                    'wind_speed': wind_speed,
                    'pressure': pressure
                }
                
                # Send alert notification
                send_asthma_alert(user_info, asthma_risk, environmental_data)
            
            # Get health advice
            advice = self.get_health_advice(
                asthma_risk, pm25, pm10, temperature, humidity, 
                patient_age, patient_history_severe_attacks, medication_adherence,
                confidence
            )
            
            # Get feature importance
            feature_importance = get_feature_importance()
            
            # Get local symptom reports
            local_reports = get_local_symptom_reports(lat, lon, radius_km=5)
            
            # Return JSON response
            response_data = {
                'city': city,
                'pm25': pm25,
                'pm10': pm10,
                'temperature': round(temperature, 1),
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed,
                'pollen_level': pollen_level,
                'patient_age': patient_age,
                'patient_history_severe_attacks': patient_history_severe_attacks,
                'medication_adherence': round(medication_adherence, 2),
                'asthma_risk': asthma_risk,
                'confidence': round(confidence, 2) if confidence else None,
                'probabilities': {k: round(v, 2) for k, v in probabilities.items()} if probabilities else None,
                'advice': advice,
                'feature_importance': feature_importance,
                'xai_explanations': xai_explanations,
                'local_symptom_reports': local_reports[:10]  # Limit to 10 most recent
            }
            
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def get_health_advice(self, risk_level, pm25, pm10, temp, humidity, 
                         patient_age, patient_history_severe_attacks, medication_adherence,
                         confidence=None):
        """Generate health advice based on risk level and conditions"""
        base_advice = f"Air quality conditions: PM2.5={pm25:.1f} μg/m³, PM10={pm10:.1f} μg/m³, Temperature={temp:.1f}°C, Humidity={humidity:.1f}%."
        
        if confidence:
            base_advice += f" Prediction confidence: {confidence*100:.0f}%."
        
        risk_specific_advice = {
            'High': f"High risk detected. Consider staying indoors during peak pollution hours. "
                   f"Patient age: {patient_age} years, History of severe attacks: {patient_history_severe_attacks}, "
                   f"Medication adherence: {medication_adherence*100:.0f}%. Please consult your healthcare provider immediately.",
            'Moderate': f"Moderate risk detected. Limit outdoor activities during peak pollution hours. "
                       f"Patient age: {patient_age} years, History of severe attacks: {patient_history_severe_attacks}, "
                       f"Medication adherence: {medication_adherence*100:.0f}%. Monitor your symptoms closely.",
            'Low': f"Low risk. Enjoy outdoor activities but stay hydrated. "
                  f"Patient age: {patient_age} years, History of severe attacks: {patient_history_severe_attacks}, "
                  f"Medication adherence: {medication_adherence*100:.0f}%. Continue your regular routine."
        }
        
        return base_advice + " " + risk_specific_advice.get(risk_level, "General advice: Monitor your symptoms and follow your asthma action plan.")

@method_decorator(csrf_exempt, name='dispatch')
class MedicationReminderView(View):
    def post(self, request):
        """Handle medication reminder requests"""
        try:
            data = json.loads(request.body)
            
            user_info = {
                'name': data.get('name', 'User'),
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'device_token': data.get('device_token', '')
            }
            
            medication_name = data.get('medication_name', 'Your medication')
            dosage_time = data.get('dosage_time', 'now')
            
            success = send_medication_reminder(user_info, medication_name, dosage_time)
            
            return JsonResponse({
                'success': success,
                'message': 'Medication reminder sent' if success else 'Failed to send medication reminder'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class SymptomReportView(View):
    def post(self, request):
        """Handle symptom reports from users"""
        try:
            data = json.loads(request.body)
            
            # Save the symptom report
            report_id = save_symptom_report(data)
            
            # Process symptom report
            symptoms = data.get('symptoms', {})
            location = data.get('location', {})
            user_id = data.get('user_id', 'anonymous')
            
            report_summary = {
                'user_id': user_id,
                'timestamp': data.get('timestamp', ''),
                'symptoms': symptoms,
                'location': location,
                'severity': self.calculate_severity(symptoms)
            }
            
            return JsonResponse({
                'success': True,
                'message': 'Symptom report received',
                'report_id': report_id
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def calculate_severity(self, symptoms):
        """Calculate severity based on reported symptoms"""
        severity_score = 0
        severity_map = {
            'wheezing': 3,
            'shortness_of_breath': 3,
            'chest_tightness': 2,
            'coughing': 2,
            'difficulty_sleeping': 1
        }
        
        for symptom, present in symptoms.items():
            if present and symptom in severity_map:
                severity_score += severity_map[symptom]
        
        if severity_score >= 5:
            return 'High'
        elif severity_score >= 3:
            return 'Moderate'
        else:
            return 'Low'