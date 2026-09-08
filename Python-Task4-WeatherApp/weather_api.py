print("WEATHER_API.PY STARTED")
import requests
import os
from dotenv import load_dotenv



# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")

print("API KEY LOADED:", bool(API_KEY))
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


print("FUNCTION DEFINITION REACHED")
def get_current_weather(city):
    """
    Fetch current weather information for a city.
    """

    if not API_KEY:
        return {
            "success": False,
            "error": "API key not found. Please check your .env file."
        }

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        # City not found
        if response.status_code == 404:
            return {
                "success": False,
                "error": "City not found. Please check the city name."
            }

        # Invalid API key
        if response.status_code == 401:
            return {
                "success": False,
                "error": "Invalid API key."
            }

        # Other API errors
        response.raise_for_status()

        data = response.json()

        return {
            "success": True,
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timed out. Please try again."
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Network error. Please check your internet connection."
        }

    except requests.exceptions.RequestException as error:
        return {
            "success": False,
            "error": f"Weather service error: {error}"
        }

    except (KeyError, ValueError):
        return {
            "success": False,
            "error": "Invalid response received from the weather service."
        }

    print("BEFORE TEST BLOCK")

if __name__ == "__main__":
    print("INSIDE TEST BLOCK")

    result = get_current_weather("Chandigarh")

    print("API RESPONSE:")
    print(result)

    print("Test finished.")

