# AsthmaShield - AI-Powered Asthma Management Platform

AsthmaShield is an advanced AI-powered platform designed to predict asthma risk levels based on real-time environmental data, providing personalized health recommendations and preventive measures.

## 🌟 Key Features

### 🤖 AI-Powered Risk Prediction
- Real-time asthma risk assessment based on environmental factors
- Machine learning models trained on comprehensive asthma datasets
- Personalized predictions based on patient history and medication adherence

### 🔍 Explainable AI (XAI) with SHAP & LIME
- **SHAP (SHapley Additive exPlanations)**: Understand feature contributions to predictions
- **LIME (Local Interpretable Model-agnostic Explanations)**: Get local explanations for individual predictions
- Transparent AI decisions for healthcare professionals and patients

### 🏥 Clinical & Preventive Intelligence
- **Nearest Medical Support**: Integration with AWS Location Service to find nearby hospitals and clinics
- **Medication Reminders**: Personalized alerts via email, SMS, and push notifications
- **Early Warning Alerts**: Proactive notifications when asthma risk is high in your area

### 🌍 Crowdsource Data Collection
- **Symptom Reporting**: Users can report symptoms to improve model accuracy
- **Real-time Validation**: Community-driven data validation for accuracy
- **Health Department Partnerships**: Collaborate with NGOs and health departments for air quality awareness

### 🎮 Gamification & Engagement
- **Asthma Buddy Avatar**: Child-friendly companion for medication adherence
- **Health Tracking**: Progress monitoring and achievement badges
- **Family Dashboard**: Remote monitoring for caregivers and family members

## 🏗️ Architecture

### Backend (Django)
- RESTful API for predictions and data management
- PostgreSQL database for user and health data
- Redis for caching and real-time features
- Celery for background tasks and notifications

### Frontend (Streamlit)
- Interactive dashboard for risk assessment
- Real-time environmental data visualization
- Personalized health recommendations
- Symptom reporting interface

### AI/ML Components
- TensorFlow and scikit-learn for predictive modeling
- SHAP and LIME for explainable AI
- Real-time data processing and analysis

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AsthmaShield
```

2. Set up the backend environment:
```bash
cd backend
python -m venv venv
# On Windows
.\venv\Scripts\Activate.ps1
# On macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up the frontend environment:
```bash
cd frontend
python -m venv venv
# On Windows
.\venv\Scripts\Activate.ps1
# On macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

4. Configure environment variables:
Create `.env` files in both backend and frontend directories with your API keys and configuration.

### Running the Application

1. Start the backend server:
```bash
cd backend
python manage.py runserver
```

2. Start the frontend dashboard:
```bash
cd frontend
streamlit run app.py
```

## 🧠 AI Model Features

### Enhanced Prediction Accuracy
- Multi-factor environmental analysis (PM2.5, PM10, temperature, humidity, etc.)
- Patient-specific factors (age, medical history, medication adherence)
- Data augmentation techniques for improved model robustness

### Explainable AI (XAI)
- **SHAP Values**: Global and local feature importance
- **LIME Explanations**: Instance-specific model interpretations
- Clear understanding of why a particular risk level was predicted

### Clinical Intelligence
- Integration with AWS Location Service for nearest medical facility identification
- Automated medication reminders via multiple channels
- Early warning system with customizable alert thresholds

## 🤝 Crowdsource Data Initiative

### Symptom Reporting
- Anonymous symptom reporting to improve model accuracy
- Geotagged data for location-based risk mapping
- Real-time data validation through community feedback

### Partnerships
- Collaboration with health departments for official data sources
- NGO partnerships for air quality awareness campaigns
- Research institution data sharing for model improvement

## 🔧 API Endpoints

### Prediction API
- `GET /api/predict/` - Get asthma risk prediction for a location
- `POST /api/medication-reminder/` - Set medication reminders
- `POST /api/symptom-report/` - Submit symptom reports

### Data Collection
- Real-time environmental data from OpenWeatherMap
- Air quality data from OpenWeather Air Pollution API
- User-generated symptom reports for model enhancement

## 📱 Frontend Features

### Dashboard
- Interactive risk map visualization
- Real-time environmental data cards
- Personalized health recommendations
- XAI explanation interface

### Notification System
- Email alerts for high-risk conditions
- SMS notifications for immediate warnings
- Push notifications for medication reminders

### Community Features
- Symptom reporting form
- Local trend visualization
- Health department announcements

## 🛡️ Security & Compliance

- HIPAA/GDPR compliant data handling
- End-to-end encryption for sensitive data
- Secure authentication and authorization
- Regular security audits and updates

## 📈 Future Enhancements

- IoT device integration for smart home automation
- Voice-based attack prediction using cough analysis
- Advanced gamification features for children
- Integration with wearable health devices
- Telemedicine consultation features

## 🤓 Contributing

We welcome contributions from the community! Please read our contributing guidelines before submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenWeatherMap for environmental data APIs
- TensorFlow and scikit-learn for machine learning libraries
- SHAP and LIME for explainable AI frameworks
- All contributors and partners in the asthma research community