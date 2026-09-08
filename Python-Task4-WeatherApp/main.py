import tkinter as tk
from tkinter import messagebox
from weather_api import get_current_weather

# -----------------------------

# Main Window

# -----------------------------

root = tk.Tk()
root.title("Weather App")
root.geometry("700x600")
root.resizable(False, False)

# -----------------------------

# Title

# -----------------------------

title_label = tk.Label(
root,
text="🌦️ Weather Dashboard",
font=("Arial", 24, "bold")
)
title_label.pack(pady=20)

# -----------------------------

# City Input

# -----------------------------

city_label = tk.Label(
root,
text="Enter City Name:",
font=("Arial", 12)
)
city_label.pack(pady=(10, 5))

city_entry = tk.Entry(
root,
width=35,
font=("Arial", 14)
)
city_entry.pack(pady=5)

# -----------------------------

# Get Weather Button

# -----------------------------

def get_weather():
    
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning(
            "Input Error",
            "Please enter a city name."
        )
        return

    result = get_current_weather(city)

    if not result["success"]:
        messagebox.showerror(
            "Weather Error",
            result["error"]
        )
        return

    weather_label.config(
        text=f"📍 {result['city']}, {result['country']}\n"
             f"🌤️ {result['description'].title()}"
    )

    temperature_label.config(
        text=f"🌡️ Temperature: {result['temperature']:.1f} °C"
    )

    humidity_label.config(
        text=f"💧 Humidity: {result['humidity']}%"
    )

    wind_label.config(
        text=f"💨 Wind Speed: {result['wind_speed']} m/s"
    )


get_button = tk.Button(
root,
text="Get Weather",
font=("Arial", 12, "bold"),
padx=20,
pady=8,
command=get_weather
)
get_button.pack(pady=15)

# -----------------------------

# Weather Result Area

# -----------------------------

weather_label = tk.Label(
root,
text="Enter a city to check the weather.",
font=("Arial", 16),
justify="center"
)
weather_label.pack(pady=30)

# -----------------------------

# Temperature

# -----------------------------

temperature_label = tk.Label(
root,
text="Temperature: -- °C",
font=("Arial", 14)
)
temperature_label.pack(pady=5)

# -----------------------------

# Humidity

# -----------------------------

humidity_label = tk.Label(
root,
text="Humidity: -- %",
font=("Arial", 14)
)
humidity_label.pack(pady=5)

# -----------------------------

# Wind Speed

# -----------------------------

wind_label = tk.Label(
root,
text="Wind Speed: -- m/s",
font=("Arial", 14)
)
wind_label.pack(pady=5)

# -----------------------------

# Start Application

# -----------------------------

root.mainloop()
