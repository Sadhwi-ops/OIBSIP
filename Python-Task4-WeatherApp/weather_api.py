"""Small, dependency-free wrapper around the OpenWeather current-weather API."""

import json
import os
import socket
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def _get_api_key():
    """Read API_KEY from environment first, then from this project's .env file."""
    key = os.getenv("API_KEY")
    if key:
        return key.strip()

    env_path = Path(__file__).with_name(".env")
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return None


def _local_time(timestamp, offset):
    """Return a friendly local time using OpenWeather's UTC offset."""
    return datetime.utcfromtimestamp(timestamp + offset).strftime("%I:%M %p").lstrip("0")


def get_current_weather(city):
    """Fetch normalized current weather data for *city* in metric units."""
    api_key = _get_api_key()
    if not api_key:
        return {"success": False, "error": "API key not found. Add API_KEY to your .env file."}

    try:
        query = urlencode({"q": city, "appid": api_key, "units": "metric"})
        with urlopen(f"{BASE_URL}?{query}", timeout=12) as response:
            data = json.load(response)
        main, weather, wind, system = data["main"], data["weather"][0], data["wind"], data["sys"]
        offset = data.get("timezone", 0)
        return {
            "success": True,
            "city": data["name"], "country": system["country"],
            "temperature": main["temp"], "feels_like": main["feels_like"],
            "temp_min": main.get("temp_min"), "temp_max": main.get("temp_max"),
            "humidity": main["humidity"], "pressure": main.get("pressure"),
            "visibility": round(data.get("visibility", 0) / 1000, 1),
            "description": weather["description"], "condition": weather["main"],
            "wind_speed": wind["speed"],
            "sunrise": _local_time(system["sunrise"], offset),
            "sunset": _local_time(system["sunset"], offset),
        }
    except HTTPError as error:
        if error.code == 404:
            return {"success": False, "error": "City not found. Try a city name such as Mumbai or London."}
        if error.code == 401:
            return {"success": False, "error": "Your OpenWeather API key is invalid or not activated yet."}
        return {"success": False, "error": "Weather service is unavailable right now. Please try again shortly."}
    except (socket.timeout, TimeoutError):
        return {"success": False, "error": "The request timed out. Please try again."}
    except URLError:
        return {"success": False, "error": "Network error. Check your internet connection and try again."}
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return {"success": False, "error": "The weather service returned an unexpected response."}
