# 🚀 AsthmaShield Backend (Django)

This is the backend API for the AsthmaShield application, built with Django.

## 🏗️ Architecture

### Tech Stack
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (default)
- **ML**: scikit-learn, pandas, numpy
- **Authentication**: Django built-in auth
- **Environment**: python-dotenv

### Project Structure
```
backend/
├── asthmashield/           # Django project settings
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── asthmashield_app/       # Main application
│   ├── models.py           # Database models
│   ├── views.py            # API views
│   ├── urls.py             # App URL configuration
│   └── ml_model/           # Machine learning models
├── datasets/               # Training data
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+

### Setup

1. **Activate virtual environment**
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** with the required environment variables:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   OPENWEATHER_API=your-openweather-api-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

4. **Initialize the database**
   ```bash
   python manage.py migrate
   ```

5. **Train the ML models**
   ```bash
   python train_model.py
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at http://127.0.0.1:8000.

## 🧠 Machine Learning Models

AsthmaShield supports multiple ML models for asthma risk prediction:

- **Random Forest** (default) - Robust ensemble learning
- **Logistic Regression** - Interpretable linear model

### Training Models
```bash
# Train Random Forest (default)
python train_model.py

# Train Logistic Regression
python train_model.py --model logistic_regression
```

### Model Files
- `asthmashield_app/ml_model/random_forest_model.pkl` - Trained Random Forest model
- `asthmashield_app/ml_model/label_encoder.pkl` - Label encoder for risk levels

## 🌐 API Endpoints

- `GET /api/predict/?city=<city>&patient_age=<age>&patient_history_severe_attacks=<count>&medication_adherence=<0-1>` - Predict asthma risk for a city with patient information

### Example Request
```bash
curl "http://127.0.0.1:8000/api/predict/?city=Pune&patient_age=35&patient_history_severe_attacks=2&medication_adherence=0.8"
```

### Example Response
```json
{
  "city": "Pune",
  "pm25": 6.12,
  "pm10": 6.87,
  "temperature": 26.34,
  "humidity": 71,
  "pressure": 1010,
  "wind_speed": 3.88,
  "pollen_level": 50,
  "patient_age": 35,
  "patient_history_severe_attacks": 2,
  "medication_adherence": 0.8,
  "asthma_risk": "Moderate",
  "advice": "Air quality conditions: PM2.5=6.1 μg/m³, PM10=6.9 μg/m³, Temperature=26.3°C, Humidity=71.0%. Moderate risk detected. Limit outdoor activities during peak pollution hours. Patient age: 35 years, History of severe attacks: 2, Medication adherence: 80%. Monitor your symptoms closely."
}
```

## 📊 Dataset

The system uses a comprehensive dataset with environmental and patient features stored in `datasets/asthma_data.csv`.

### Features
- **Environmental**: PM2.5, PM10, temperature, humidity, pollen_level, wind_speed, pressure
- **Patient**: patient_age, patient_history_severe_attacks, medication_adherence
- **Target**: asthma_risk (Low, Moderate, High)

## 🛠️ Development

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Testing
```bash
# Run tests
python manage.py test
```

## 📄 License

This project is licensed under the MIT License.
