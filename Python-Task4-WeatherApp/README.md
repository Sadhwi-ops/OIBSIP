# Nimbus Weather Dashboard

A polished desktop weather dashboard built with Python and Tkinter. It uses the OpenWeather API to show live conditions for any city.

## Highlights

- Modern dark dashboard with condition-aware accent themes
- Smooth loading state; requests run in the background so the UI stays responsive
- Temperature, feels-like temperature, humidity, wind, visibility and pressure
- Local sunrise and sunset times
- Live clock and one-click recent city searches
- Clear feedback for missing keys, invalid cities and network issues

## Setup

Create a `.env` file in this folder:

```env
API_KEY=your_openweather_api_key
```

Get a free key from [OpenWeather](https://openweathermap.org/api), then start the app:

```bash
python main.py
```

Enter a city, press **Enter** or click **Search**. Recent searches remain available during the current session.

## Project structure

```text
Python-Task4-WeatherApp/
├── main.py          # Tkinter dashboard and UI behavior
├── weather_api.py   # Dependency-free OpenWeather API client
├── requirements.txt # No installation required
└── .env             # Your private API key (not committed)
```
