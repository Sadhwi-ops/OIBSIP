import speech_recognition as sr
import asyncio
import edge_tts
import pygame
import os
import datetime
from commands import web_search, detect_intent
from email_sender import send_email
from getpass import getpass
from reminder import set_reminder
from weather import get_weather
from knowledge import answer_question
from custom_commands import run_custom_command


# ---------------- SPEAK FUNCTION ----------------

async def speak(text):
    filename = "speech.mp3"

    communicate = edge_tts.Communicate(
        text,
        "en-US-AriaNeural"
    )

    await communicate.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.quit()


# ---------------- LISTEN FUNCTION ----------------

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n🎙️ Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("🎙️ Speak now...")

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

        except sr.WaitTimeoutError:
            print("Assistant: I didn't hear anything.")
            asyncio.run(speak("I didn't hear anything."))
            return ""

    try:
        command = recognizer.recognize_google(audio)

        print("You said:", command)

        return command.lower()

    except sr.UnknownValueError:
        print("Assistant: Sorry, I didn't understand that.")
        asyncio.run(speak("Sorry, I didn't understand that."))
        return ""

    except sr.RequestError:
        print("Assistant: Speech recognition service is unavailable.")
        asyncio.run(
            speak("Speech recognition service is unavailable.")
        )
        return ""

# ---------------- MAIN ASSISTANT ----------------

print("===================================")
print("       KIZZIEE VOICE ASSISTANT")
print("===================================")

asyncio.run(speak("Hello Kizziee! I am your voice assistant."))


while True:

    command = listen()
    intent = detect_intent(command)
    print("Detected intent:", intent)
    custom_response = run_custom_command(command)

    if custom_response:
      print("Assistant:", custom_response)
      asyncio.run(speak(custom_response))
      continue

    if command == "":
        continue

    if intent == "greeting":
        print("Assistant: Hello Kizziee!")
        asyncio.run(speak("Hello Kizziee!"))

    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%I:%M %p")

        print("Assistant:", current_time)

        asyncio.run(
            speak("The current time is " + current_time)
        )

    elif intent == "date":
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        print("Assistant:", current_date)
        asyncio.run(speak("Today's date is " + current_date))

    elif intent == "search":
        query = command.replace("search", "").strip()

        if query:
           response = web_search(query)
           print("Assistant:", response)
           asyncio.run(speak(response))
        else:
           print("Assistant: What should I search for?")
           asyncio.run(speak("What should I search for?"))

    elif intent == "email":
        print("Assistant: Please enter your email address.")
        sender_email = input("Your email: ")

        print("Assistant: Please enter your app password.")
        app_password = getpass("App password: ")

        print("Assistant: Who should I send the email to?")
        receiver_email = input("Receiver email: ")

        print("Assistant: What is the subject?")
        subject = input("Subject: ")

        print("Assistant: What should the email say?")
        message = input("Message: ")

        success = send_email(
        sender_email,
        app_password,
        receiver_email,
        subject,
        message
    )

        if success:
           print("Assistant: Email sent successfully!")
           asyncio.run(speak("Email sent successfully!"))
        else:
           print("Assistant: I couldn't send the email.")
           asyncio.run(speak("I couldn't send the email."))

    elif intent == "reminder":

      print("Assistant: What should I remind you about?")
      reminder_message = input("Reminder: ")

      print("Assistant: How many seconds from now?")
      seconds = int(input("Seconds: "))

      response = set_reminder(reminder_message, seconds)

      print("Assistant:", response)
      asyncio.run(speak(response))

    elif intent == "knowledge":
      response = answer_question(command)
      print("Assistant:", response)
      asyncio.run(speak(response))

    elif intent == "weather":
      print("Assistant: Which city?")
      city = input("City: ")

      response = get_weather(city)

      print("Assistant:", response)
      asyncio.run(speak(response))

    elif intent == "exit":
        print("Assistant: Goodbye!")
        asyncio.run(speak("Goodbye!"))
        break

    else:
        asyncio.run(speak("I don't know that command yet."))