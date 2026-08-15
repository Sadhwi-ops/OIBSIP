import json
import webbrowser


def load_custom_commands():
    try:
        with open("custom_commands.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        return {}


def run_custom_command(command):
    commands = load_custom_commands()

    command = command.lower().strip()

    if command in commands:
        webbrowser.open(commands[command])
        return f"Opening {command}."

    return None

if __name__ == "__main__":
    result = run_custom_command("open youtube")

    if result:
        print("Assistant:", result)
    else:
        print("Assistant: Custom command not found.")