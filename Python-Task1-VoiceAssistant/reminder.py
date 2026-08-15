import threading
import time
import asyncio
import edge_tts
import pygame


async def speak(text):
    filename = "reminder.mp3"

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


def set_reminder(message, seconds):

    def reminder_task():
        time.sleep(seconds)

        reminder_text = "Reminder: " + message

        print("\n🔔", reminder_text)

        asyncio.run(speak(reminder_text))

    reminder_thread = threading.Thread(
        target=reminder_task
    )

    reminder_thread.daemon = True
    reminder_thread.start()

    return "Reminder set successfully!"