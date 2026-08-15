import webbrowser
import urllib.parse


def web_search(query):
    encoded_query = urllib.parse.quote(query)

    url = "https://www.google.com/search?q=" + encoded_query

    webbrowser.open(url)

    return "Here are the search results for " + query


def detect_intent(command):
    command = command.lower().strip()

    # Greeting
    if any(word in command for word in ["hello", "hi", "hey"]):
        return "greeting"

    # Time
    if any(phrase in command for phrase in [
        "what time",
        "current time",
        "tell me the time",
        "time is it",
        "time"
    ]):
        return "time"

    # Date
    if any(phrase in command for phrase in [
        "what date",
        "today's date",
        "todays date",
        "tell me the date",
        "what day is it",
        "date"
    ]):
        return "date"

    # Weather
    if any(word in command for word in [
        "weather",
        "temperature",
        "forecast"
    ]):
        return "weather"

    # Web search
    if any(phrase in command for phrase in [
        "search for",
        "search",
        "look up",
        "google"
    ]):
        return "search"

    # Email
    if any(phrase in command for phrase in [
        "send an email",
        "send email",
        "write an email",
        "email"
    ]):
        return "email"

    # Reminder
    if any(phrase in command for phrase in [
        "set a reminder",
        "set reminder",
        "remind me",
        "reminder"
    ]):
        return "reminder"

    # Knowledge
    if any(phrase in command for phrase in [
        "what is",
        "who is",
        "who created",
        "who invented",
        "explain",
        "define"
    ]):
        return "knowledge"

    
    # Exit
    if any(word in command for word in [
        "bye",
        "goodbye",
        "exit",
        "quit"
    ]):
        return "exit"

    return "unknown"

if __name__ == "__main__":
    tests = [
        "Hello there",
        "Can you tell me what time it is?",
        "Could you tell me today's date?",
        "What's the weather like in Chandigarh?",
        "I want to search for Python tutorials",
        "Please send an email",
        "Remind me to drink water",
        "Goodbye"
    ]

    for test in tests:
        print(test, "→", detect_intent(test))