# 🌦️ Weather App
A simple Python-based Weather App that fetches and displays current weather information for a city using the OpenWeatherMap API.
## 📌 Project Overview
This project was developed as part of the **Oasis Infobyte Python Programming Internship – Task 4**.

The application provides current weather information such as:

- 🌡️ Temperature
- 🌤️ Weather condition
- 💧 Humidity
- 💨 Wind speed
- 📍 City and country

The application uses a graphical user interface built with Tkinter.

## ✨ Features

- Search weather by city name
- Displays current temperature in Celsius
- Displays weather condition
- Displays humidity
- Displays wind speed
- Handles invalid city names
- Handles invalid API keys
- Handles network errors
- Simple and user-friendly GUI

## 🛠️ Technologies Used

- Python
- Tkinter
- Requests
- OpenWeatherMap API
- python-dotenv

## 📂 Project Structure

```text
Python-Task4-WeatherApp/
│
├── main.py
├── weather_api.py
├── requirements.txt
├── README.md
└── .gitignore
⚙️ Installation
1. Clone the repository
git clone https://github.com/Sadhwi-ops/OIBSIP.git
2. Navigate to the project
cd OIBSIP/Python-Task4-WeatherApp
3. Install the required packages
pip install -r requirements.txt
🔑 API Key Setup

This project uses the OpenWeatherMap API.

Create a .env file inside the project folder and add:

API_KEY=your_api_key_here

The .env file is excluded from Git using .gitignore to keep the API key private.

▶️ How to Run

Run the following command:

python main.py

Enter a city name and click Get Weather to view the current weather information.

🖥️ Example

The application displays information such as:

📍 Chandigarh, IN
🌤️ Clear Sky
🌡️ Temperature: 28.7 °C
💧 Humidity: 64%
💨 Wind Speed: 2.97 m/s
🎓 Internship

Organization: Oasis Infobyte
Track: Python Programming
Task: Task 4 – Basic Weather App

👩‍💻 Author

Sadhwi