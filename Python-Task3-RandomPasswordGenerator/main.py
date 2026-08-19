import tkinter as tk
import secrets
import string
import pyperclip
from tkinter import messagebox


# ---------------- PASSWORD HISTORY ----------------

password_history = []


# ---------------- PASSWORD STRENGTH ----------------

def calculate_strength(password):
    length = len(password)

    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_number = any(char.isdigit() for char in password)
    has_symbol = any(char in string.punctuation for char in password)

    diversity = sum([
        has_uppercase,
        has_lowercase,
        has_number,
        has_symbol
    ])

    if length >= 12 and diversity >= 3:
        return "Strong"

    elif length >= 10 and diversity >= 2:
        return "Medium"

    else:
        return "Weak"


# ---------------- COPY PASSWORD ----------------

def copy_password():
    password = password_result.cget("text")

    if password == "Your password will appear here":
        messagebox.showwarning(
            "No Password",
            "Please generate a password first."
        )
        return

    pyperclip.copy(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard!"
    )


# ---------------- UPDATE HISTORY ----------------

def update_history(password):

    password_history.append(password)

    # Keep only the last 5 passwords
    if len(password_history) > 5:
        password_history.pop(0)

    # Clear history display
    history_text.delete("1.0", tk.END)

    # Display passwords
    for index, saved_password in enumerate(
        password_history,
        start=1
    ):
        history_text.insert(
            tk.END,
            f"{index}. {saved_password}\n"
        )


# ---------------- GENERATE PASSWORD ----------------

def generate_password():

    # Get password length
    try:
        length = int(length_entry.get())

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number for password length."
        )
        return

    # Minimum password length
    if length < 8:
        messagebox.showerror(
            "Invalid Length",
            "Password length must be at least 8 characters."
        )
        return

    # Store selected character groups
    selected_groups = []

    if uppercase_var.get():
        selected_groups.append(string.ascii_uppercase)

    if lowercase_var.get():
        selected_groups.append(string.ascii_lowercase)

    if numbers_var.get():
        selected_groups.append(string.digits)

    if symbols_var.get():
        selected_groups.append(string.punctuation)

    # At least two character types required
    if len(selected_groups) < 2:
        messagebox.showerror(
            "Invalid Selection",
            "Please select at least two character types."
        )
        return

    # Password must be long enough
    if length < len(selected_groups):
        messagebox.showerror(
            "Invalid Length",
            "Password length is too short for the selected character types."
        )
        return

    # ---------------- AMBIGUOUS CHARACTER FILTER ----------------

    ambiguous_characters = "0Ol1"

    filtered_groups = []

    for group in selected_groups:

        if ambiguous_var.get():

            filtered_group = "".join(
                char for char in group
                if char not in ambiguous_characters
            )

        else:
            filtered_group = group

        filtered_groups.append(filtered_group)

    # Make sure every selected group still contains characters
    for group in filtered_groups:

        if not group:
            messagebox.showerror(
                "Invalid Selection",
                "The selected character types cannot be used with the current settings."
            )
            return

    # ---------------- GUARANTEE CHARACTER TYPES ----------------

    password_characters = []

    for group in filtered_groups:

        password_characters.append(
            secrets.choice(group)
        )

    # ---------------- COMBINED CHARACTER POOL ----------------

    all_characters = "".join(filtered_groups)

    # Fill remaining password positions
    remaining_length = length - len(password_characters)

    for _ in range(remaining_length):

        password_characters.append(
            secrets.choice(all_characters)
        )

    # ---------------- SECURE SHUFFLE ----------------

    secrets.SystemRandom().shuffle(password_characters)

    # Convert list into a string
    password = "".join(password_characters)

    # ---------------- DISPLAY PASSWORD ----------------

    password_result.config(
        text=password
    )

    # ---------------- PASSWORD STRENGTH ----------------

    strength = calculate_strength(password)

    strength_result.config(
        text=f"Strength: {strength}"
    )

    # ---------------- UPDATE HISTORY ----------------

    update_history(password)


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Random Password Generator")

root.geometry("550x650")


# ---------------- PASSWORD LENGTH ----------------

length_label = tk.Label(
    root,
    text="Password Length:"
)

length_label.pack(pady=5)


length_entry = tk.Entry(root)

length_entry.pack(pady=5)


# ---------------- CHARACTER TYPES ----------------

type_label = tk.Label(
    root,
    text="Choose Character Types:"
)

type_label.pack(pady=5)


# Checkbox variables

uppercase_var = tk.BooleanVar()

lowercase_var = tk.BooleanVar()

numbers_var = tk.BooleanVar()

symbols_var = tk.BooleanVar()

ambiguous_var = tk.BooleanVar()


# ---------------- CHECKBOXES ----------------

uppercase_check = tk.Checkbutton(
    root,
    text="Uppercase Letters",
    variable=uppercase_var
)

uppercase_check.pack()


lowercase_check = tk.Checkbutton(
    root,
    text="Lowercase Letters",
    variable=lowercase_var
)

lowercase_check.pack()


numbers_check = tk.Checkbutton(
    root,
    text="Numbers",
    variable=numbers_var
)

numbers_check.pack()


symbols_check = tk.Checkbutton(
    root,
    text="Symbols",
    variable=symbols_var
)

symbols_check.pack()


ambiguous_check = tk.Checkbutton(
    root,
    text="Exclude ambiguous characters (0, O, l, 1)",
    variable=ambiguous_var
)

ambiguous_check.pack(pady=5)


# ---------------- GENERATE BUTTON ----------------

generate_button = tk.Button(
    root,
    text="Generate Password",
    command=generate_password
)

generate_button.pack(pady=10)


# ---------------- PASSWORD RESULT ----------------

password_result = tk.Label(
    root,
    text="Your password will appear here"
)

password_result.pack(pady=5)


# ---------------- STRENGTH RESULT ----------------

strength_result = tk.Label(
    root,
    text="Strength: Not generated yet"
)

strength_result.pack(pady=5)


# ---------------- COPY BUTTON ----------------

copy_button = tk.Button(
    root,
    text="Copy Password",
    command=copy_password
)

copy_button.pack(pady=5)


# ---------------- HISTORY ----------------

history_label = tk.Label(
    root,
    text="Last 5 Generated Passwords:"
)

history_label.pack(pady=10)


history_text = tk.Text(
    root,
    height=6,
    width=55
)

history_text.pack(pady=5)


# ---------------- START APPLICATION ----------------

root.mainloop()