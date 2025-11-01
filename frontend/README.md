# 🌬️ AsthmaShield Frontend (Streamlit)

This is the frontend for the AsthmaShield application, built with Streamlit.

## 🏗️ Architecture

### Tech Stack
- **Framework**: Streamlit 1.28.0
- **Mapping**: folium, streamlit-folium
- **Environment**: python-dotenv
- **API Client**: requests

### Project Structure
```
frontend/
├── app.py                 # Main Streamlit application
├── components/            # UI components
│   ├── map_component.py   # Map visualization component
│   └── weather_card.py    # Weather data display component
├── assets/                # Static assets
│   ├── style.css          # Custom CSS styles
│   └── logo.txt           # Logo placeholder
├── requirements.txt       # Python dependencies
└── README.md             # This file
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
   OPENWEATHER_API=your-openweather-api-key
   GEMINI_API_KEY=your-gemini-api-key
   ```

4. **Run the Streamlit application**
   ```bash
   streamlit run app.py
   ```

The application will be available at http://localhost:8501.

## 🎯 Features

### Interactive Dashboard
- City selection for asthma risk prediction
- Patient information input (age, history of severe attacks, medication adherence)
- Real-time environmental data display
- Asthma risk level visualization
- AI-generated health advice

### Map Visualization
- Interactive map showing risk zones
- OpenStreetMap integration
- Location-based risk markers

### Data Display
- Temperature, humidity, and air quality metrics
- Wind speed and atmospheric pressure
- Patient-specific information panels

## 🌐 API Integration

The frontend communicates with the Django backend API at `http://127.0.0.1:8000` to fetch predictions and health advice.

### API Endpoint
- `GET /api/predict/` - Fetch asthma risk prediction

## 🎨 UI Components

### Weather Cards
Reusable components for displaying environmental and patient data with consistent styling.

### Map Component
Interactive map visualization using folium and streamlit-folium.

## 🎨 Custom Styling

The application uses custom CSS styles defined in `assets/style.css` for consistent theming and improved user experience.

## 📄 License

This project is licensed under the MIT License.
