# Python Voice Assistant

A Python-based voice assistant developed as part of the Oasis Infobyte Python Internship.

The assistant accepts spoken commands through a microphone, understands different types of requests, performs useful actions, and provides spoken responses using text-to-speech.

## Project Objective

The objective of this project is to build a functional voice assistant using Python that can:

- Capture voice input from the microphone
- Understand natural language commands
- Respond using text-to-speech
- Provide time and date information
- Perform web searches
- Fetch live weather information
- Send emails
- Set timed reminders
- Answer general knowledge questions
- Execute user-defined custom commands

## Features

### Beginner Features

- Voice input using `SpeechRecognition`
- Predefined greeting for hello commands
- Current time and date
- Web search using a web browser
- Graceful handling of speech recognition errors
- Text-to-speech responses using `pyttsx3`

### Advanced Features

- Natural language intent detection
- Email sending using `smtplib`
- Timed reminders with audible alerts
- Live weather information using the Open-Meteo API
- General knowledge answers using a local knowledge base
- Custom commands using a JSON configuration file
- Privacy and data-processing documentation

## Technologies Used

- Python
- SpeechRecognition
- pyttsx3
- datetime
- webbrowser
- urllib
- requests
- smtplib
- JSON
- Open-Meteo API

## Project Structure

```text
Python-Task1-VoiceAssistant/
│
├── main.py
├── commands.py
├── weather.py
├── reminder.py
├── email_sender.py
├── knowledge.py
├── custom_commands.py
├── custom_commands.json
├── requirements.txt
├── test.py
└── README.md
## How It Works

```text
User speaks
     ↓
Microphone captures voice
     ↓
SpeechRecognition converts speech to text
     ↓
Intent detection identifies the requested action
     ↓
Appropriate module performs the action
     ↓
Assistant generates a response
     ↓
pyttsx3 speaks the response

Installation
1. Install Python

Python 3.12 or a compatible Python version is recommended.

Check your Python installation:

py --version

or:

py -3.12 --version
2. Install Dependencies

Open a terminal inside the project folder and run:

py -3.12 -m pip install -r requirements.txt
3. Run the Assistant

Run:

py -3.12 main.py

Make sure your microphone is connected and available.

Example Voice Commands

The assistant can understand natural language commands such as:

"Hello"


"Could you tell me what time it is?"


"Can you tell me today's date?"


"Search for Python tutorials"


"What's the weather like in Chandigarh?"


"What is Python?"


"Who created Python?"


"Open YouTube"


"Please send an email"


"Remind me to drink water"


"Goodbye"
Weather Feature

The weather feature uses the Open-Meteo API.

The assistant:

Receives the city name.
Finds the city's latitude and longitude using geocoding.
Requests current weather information.
Interprets the weather code.
Reads the result aloud.

No Open-Meteo API key is required for the implementation used in this project.

Email Feature

The email feature uses Python's smtplib.

The assistant can collect:

Recipient email address
Email app password
Message content

The credentials are used to authenticate with the email service and send the message.

For security, passwords should not be stored directly in the source code or uploaded to GitHub.

Reminder Feature

The reminder system accepts a reminder message and a specified duration.

After the duration expires, the assistant provides an audible reminder notification.

General Knowledge Feature

The assistant contains a local knowledge base for answering selected general knowledge questions.

Examples include:

What is Python?
What is artificial intelligence?
What is machine learning?
What is GitHub?
Who created Python?

The knowledge base can be expanded with additional questions and answers.

Custom Commands

Custom commands are stored in:

custom_commands.json

Example:

{
    "open youtube": "https://www.youtube.com",
    "open github": "https://github.com",
    "open python": "https://www.python.org"
}

New commands can be added to the JSON configuration without modifying the Python implementation.

Error Handling

The assistant handles situations such as:

Speech that cannot be understood
No speech detected
Network connection problems
Unknown commands
Missing or invalid custom command configuration
Invalid weather requests

Instead of terminating unexpectedly, the assistant attempts to provide a useful response.

Privacy Considerations

This project processes voice input through the microphone and converts recognized speech into text for command processing.

Data Processed

The assistant may process:

Spoken commands
Recognized text from those commands
City names for weather requests
Email addresses and email messages when the email feature is used
Reminder messages and durations
Custom command information stored in the configuration file
How the Data Is Used
Voice input is used to determine the requested command.
Weather-related city information is sent to the Open-Meteo service to retrieve weather information.
Email information is used to send an email through the configured email service.
Custom commands are read from the local JSON configuration file.
The local knowledge base is processed locally.
Security

Email passwords or app passwords should not be hard-coded into the project or committed to GitHub.

Sensitive credentials should be kept private and should never be included in screenshots, source code, or public repositories.

This project does not intentionally store a permanent history of users' spoken commands.

Limitations
The local knowledge base contains a limited set of questions.
Speech recognition accuracy depends on microphone quality and surrounding noise.
Internet access is required for weather and web-search functionality.
Email functionality requires valid email-service credentials.
Custom commands currently focus on configured browser actions.
Future Improvements

Possible future improvements include:

Larger natural language understanding models
More extensive knowledge-base support
More customizable voice commands
Integration with additional APIs
Smart-home device control
Improved conversation context
Secure environment-variable-based credential management
More advanced NLP intent classification
Internship

Developed as part of the Oasis Infobyte Python Internship.

Task: Python Voice Assistant



### ⚠️ One important thing


Make sure the final README has **both parts**:


```text
Project Objective
       ↓
Features
       ↓
Technologies
       ↓
Project Structure
       ↓
How It Works
       ↓
Installation
       ↓
Example Commands
       ↓
Weather
       ↓
Email
       ↓
Reminder
       ↓
Knowledge
       ↓
Custom Commands
       ↓
Error Handling
       ↓
Privacy Considerations  ← REQUIRED
       ↓
Limitations
       ↓
Future Improvements
       ↓
Internship