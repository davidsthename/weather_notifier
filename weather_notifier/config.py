# Stores API key and default alert thresholds for the weather monitoring app.

import streamlit as st
API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# Starting alert thresholds values in Sliders
DEFAULTS = {
    "temp_high": 35,   # Alert if temperature ≥ 35°C
    "temp_low": 0,     # Alert if temperature ≤ 0°C
    "wind_high": 50,   # Alert if wind ≥ 50 km/h
    "rain_high": 10    # Alert if rain ≥ 10 mm in last hour
}  # defaults is a dictionary
