# Contains all Streamlit UI code — layout, cards, refresh loop

import streamlit as st  # Imports the streamlit framework library
import time
from datetime import datetime
from weather import get_current_weather  # imports get_current_weather function
from alerts import check_and_alert
from config import DEFAULTS  # imports default thresholds dictionary


def show_app():
    """Main function that runs the entire Streamlit app"""

    st.title("Automated Weather Notifier")
    st.markdown("**Modular • Real-time • Voice Alerts • Custom Thresholds**")

    # === Sidebar: User Settings ===
    with st.sidebar:
        st.header("Alert Thresholds")
        temp_high = st.slider("High Temperature (°C)",
                              25, 50, DEFAULTS["temp_high"])
        temp_low = st.slider("Low Temperature (°C)", -
                             20, 15, DEFAULTS["temp_low"])
        wind_high = st.slider("Strong Wind (km/h)", 30,
                              100, DEFAULTS["wind_high"])
        rain_high = st.slider("Heavy Rain (mm/h)", 5,
                              50, DEFAULTS["rain_high"])

        # refreshes stat every 5 minutes
        auto_refresh = st.checkbox("Auto-refresh every 5 minutes", True)

        cities_input = st.text_input(
            "Cities to monitor",
            "London, Tokyo, Dubai, Moscow, Delhi, New York"  # default cities to monitor
        )
        cities = [city.strip()
                  for city in cities_input.split(",") if city.strip()]

    # Store thresholds in a dictionary
    thresholds = {
        "temp_high": temp_high,
        "temp_low": temp_low,
        "wind_high": wind_high,
        "rain_high": rain_high
    }  # thresholds means the limit

    # Initialize alert tracking in session state
    if "last_alert" not in st.session_state:
        # stops the app from sending the same alert repeatedly
        st.session_state.last_alert = {}

    # Containers for dynamic content
    placeholder = st.empty()
    banner = st.empty()

    # === Main Refresh Loop ===
    while True:
        current_alerts = []   # List of active alerts this cycle
        weather_cards = []    # cards to display

        for city in cities:
            data = get_current_weather(city)

            if not data or data.get("cod") != 200:
                weather_cards.append(
                    f"#### Error **{city}** – Not found or API error")
                continue

            # Extract weather data
            # rounds the current temperature to 1 decimal place
            temp = round(data["main"]["temp"], 1)
            feels = round(data["main"]["feels_like"], 1)
            # capitalizes the first letter of the weather description
            description = data["weather"][0]["description"].capitalize()
            # converts wind speed from m/s to km/h and rounds it
            wind_kmh = round(data["wind"]["speed"] * 3.6)
            rain_1h = data.get("rain", {}).get("1h", 0)

            # Check if severe and trigger alert + voice
            alert_msg, _ = check_and_alert(
                city, data, thresholds, st.session_state.last_alert)
            if alert_msg:
                current_alerts.append(alert_msg)

            # Choose emoji based on temperature
            if temp >= temp_high:
                emoji = "Extreme heat"
            elif temp <= temp_low:
                emoji = "Freezing"
            else:
                emoji = "Sunny"

            # Create beautiful markdown card
            card = f"""
            #### {emoji} **{city}**
            **{temp}°C** – {description}
            Feels like **{feels}°C** • Wind **{wind_kmh} km/h** • Rain **{rain_1h} mm/h**
            """
            weather_cards.append(card)

        # === Update Display ===
        with placeholder.container():
            st.markdown(
                f"**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Top banner
            if current_alerts:
                banner.error("SEVERE WEATHER ALERTS ACTIVE")
                for alert in current_alerts:
                    st.error(alert)
            else:
                banner.success("All locations are safe")

            # Display cards in 3 columns
            for i in range(0, len(weather_cards), 3):
                cols = st.columns(3)
                for j in range(3):
                    idx = i + j
                    if idx < len(weather_cards):
                        with cols[j]:
                            st.markdown(weather_cards[idx])

        # Stop loop if auto-refresh disabled
        if not auto_refresh:
            st.stop()

        time.sleep(300)  # Wait 5 minutes
        st.rerun()       # Refresh the app
