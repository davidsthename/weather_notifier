# Responsible for calling OpenWeatherMap API and returning data
import requests  # this module helps us contact or call the weather API
from config import API_KEY  # Get the API key from config.py


def get_current_weather(city: str) -> dict:
    """
    Fetches current weather for a given city
    Returns: JSON data from API or None if failed
    """
    url = "http://api.openweathermap.org/data/2.5/weather"  # where to get current weather data from

    # Parameters sent to the API
    params = {
        "q": city,           # What city to get weather for
        "appid": API_KEY,    # API key for authentication
        "units": "metric"    # Get temperature in Celsius and wind in km/h
    }

    try:
        # response uses imported requests library
        response = requests.get(url, params=params, timeout=10)

        # Return data only if city was found (status 200)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        # Return None if internet down or API error
        return None
