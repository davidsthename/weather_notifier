# Handles checking for severe weather and speaking alerts
import time  # imports time module to track alert times
import streamlit as st  # Imports the streamlit framework library

# Trys to import voice libraries
try:
    from gtts import gTTS
    import os
    VOICE_ENABLED = True
except ImportError:
    VOICE_ENABLED = False


def speak(text: str):
    """Uses Google Text-to-Speech to speak the alert out loud"""
    if not VOICE_ENABLED:
        return  # skips if voice not available

    try:
        tts = gTTS(text=text, lang='en', tld="co.uk")     # Creates speech
        tts.save("alert.mp3")                # Saves as MP3
        # this will play the alert sound based on OS
        os.system("start alert.mp3" if os.name == 'nt' else "afplay alert.mp3")
        # Wait for speech to finish before deleting
        time.sleep(4)
        # Clean up file to avoid clutter and save space
        os.remove("alert.mp3")
    except:
        pass  # Ignore any voice errors


def check_and_alert(city: str, data: dict, thresholds: dict, last_alert_dict: dict) -> tuple:
    """
    Checks if weather is severe and returns alert message + whether alert was triggered
    Prevents spam by allowing only one alert per hour per condition
    """
    if not data or data.get("cod") != 200:  # not data means API call failed
        return f"Failed to fetch data for {city}", False

    temp = data["main"]["temp"]  # EXtracts current temperature
    # Wind speed in meters and coverts it to Kmh
    wind_kmh = data["wind"]["speed"] * 3.6
    # has it rained in the last hour? if yes returns"rain"
    rain_1h = data.get("rain", {}).get("1h", 0)
    # Weather description for easy matching
    description = data["weather"][0]["description"].lower()

    # different key to prevent duplicate alerts
    alert_key = f"{city}_{int(temp)}_{int(wind_kmh)}"
    current_time = time.time()  # when the last alert was sent
    # Only alert once per hour
    if alert_key in last_alert_dict and (current_time - last_alert_dict[alert_key] < 3600):
        return None, False
    alert_message = None

    # Check each severe condition
    if temp >= thresholds["temp_high"]:
        alert_message = f"EXTREME HEAT in {city}: {temp}°C"
    elif temp <= thresholds["temp_low"]:
        alert_message = f"FREEZING in {city}: {temp}°C"
    elif wind_kmh >= thresholds["wind_high"]:
        alert_message = f"STRONG WINDS in {city}: {wind_kmh:.0f} km/h"
    elif rain_1h >= thresholds["rain_high"]:
        alert_message = f"HEAVY RAIN in {city}: {rain_1h} mm/h"
    elif any(word in description for word in ["thunderstorm", "tornado", "hurricane"]):
        alert_message = f"DANGEROUS WEATHER in {city}: {data['weather'][0]['description'].capitalize()}"

    # If alert triggered → speak it and record time
    if alert_message:
        last_alert_dict[alert_key] = current_time 
        speak(alert_message)  # calls the gtts speak function
        return alert_message, True 

    return None, False
