import requests


def get_weather(city):
    try:
        # Get latitude and longitude of the city
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )

        geo_data = geo_response.json()

        if "results" not in geo_data:
            return "I couldn't find that city."

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]
        city_name = geo_data["results"][0]["name"]

        # Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,weather_code",
                "temperature_unit": "celsius"
            },
            timeout=10
        )

        weather_data = weather_response.json()

        temperature = weather_data["current"]["temperature_2m"]
        weather_code = weather_data["current"]["weather_code"]

        description = get_weather_description(weather_code)

        return (
            f"The current temperature in {city_name} "
            f"is {temperature} degrees Celsius with {description}."
        )

    except requests.RequestException:
        return "Sorry, I couldn't connect to the weather service."

    except Exception:
        return "Sorry, I couldn't get the weather right now."


def get_weather_description(code):

    if code == 0:
        return "clear sky"

    elif code in [1, 2, 3]:
        return "partly cloudy skies"

    elif code in [45, 48]:
        return "foggy conditions"

    elif code in [51, 53, 55, 56, 57]:
        return "drizzle"

    elif code in [61, 63, 65, 66, 67]:
        return "rain"

    elif code in [71, 73, 75, 77]:
        return "snow"

    elif code in [80, 81, 82]:
        return "rain showers"

    elif code in [95, 96, 99]:
        return "thunderstorms"

    else:
        return "unknown weather conditions"
    
if __name__ == "__main__":
      print(get_weather("Chandigarh"))