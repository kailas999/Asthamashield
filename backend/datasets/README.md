# AsthmaShield Dataset Documentation

## Dataset Structure

The asthma risk prediction model uses the following features:

### Environmental Features
1. **pm25** - PM2.5 particle concentration (μg/m³)
2. **pm10** - PM10 particle concentration (μg/m³)
3. **temperature** - Ambient temperature (°C)
4. **humidity** - Relative humidity (%)
5. **pollen_level** - Pollen concentration level (arbitrary units)
6. **wind_speed** - Wind speed (m/s)
7. **pressure** - Atmospheric pressure (hPa)

### Patient Features
8. **patient_age** - Age of the patient (years)
9. **patient_history_severe_attacks** - Number of severe asthma attacks in the past year
10. **medication_adherence** - Medication adherence level (0-1 scale)

## Risk Levels

The target variable has three classes:

- **Low** - Low risk of asthma symptoms
- **Moderate** - Moderate risk of asthma symptoms
- **High** - High risk of asthma symptoms

## Using the Dataset

### Training the Model

1. Ensure you have set up the Python environment with required dependencies
2. Navigate to the backend directory
3. Run the training script:
   ```bash
   python train_model.py
   ```

### Dataset Format

The dataset is stored in CSV format in `backend/datasets/asthma_data.csv` with the following structure:

```
pm25,pm10,temperature,humidity,pollen_level,wind_speed,pressure,patient_age,patient_history_severe_attacks,medication_adherence,asthma_risk
120,180,30,60,50,3.2,1013,35,2,0.8,High
90,130,28,55,40,2.8,1015,28,1,0.9,High
...
```

### Adding New Data

To add new data to the dataset:

1. Open `backend/datasets/asthma_data.csv`
2. Add new rows following the existing format
3. Retrain the model by running `python train_model.py`

## Model Information

The current model uses a Random Forest Classifier with 100 estimators. After training, the model is saved as `backend/asthmashield_app/ml_model/model.pkl`.

## Feature Engineering

For best results, consider the following when adding new data:

- PM2.5 and PM10 values typically range from 0-500 μg/m³
- Temperature values typically range from -10°C to 50°C
- Humidity values range from 0-100%
- Pollen levels are represented as arbitrary units from 0-100
- Wind speed typically ranges from 0-20 m/s
- Atmospheric pressure typically ranges from 980-1040 hPa
- Patient age typically ranges from 5-80 years
- History of severe attacks: 0-10 attacks per year
- Medication adherence: 0 (no adherence) to 1 (perfect adherence)

## Advanced ML Models

The AsthmaShield platform supports multiple machine learning models for asthma risk prediction:

1. **Logistic Regression** - For baseline performance and interpretability
2. **Random Forest** - Current default model for robust performance
3. **XGBoost** - For improved accuracy with gradient boosting
4. **Deep Neural Networks** - For complex pattern recognition

These models can analyze large volumes of electronic health records (EHR), identify at-risk individuals earlier than traditional clinical methods, and recommend tailored interventions for prevention.

## Real-Time Monitoring Features

AI-driven early warning tools are designed for continuous real-time monitoring using variables such as:
- Breathing patterns
- Symptoms tracking
- Medication use
- External triggers (weather, allergens)

These tools can alert healthcare providers and patients to impending danger.

## Ethical Considerations

When deploying machine learning in asthma care, the system carefully addresses:
- Patient privacy through data encryption and anonymization
- Potential biases through diverse dataset training
- Explainable models to build trust among clinicians and patients