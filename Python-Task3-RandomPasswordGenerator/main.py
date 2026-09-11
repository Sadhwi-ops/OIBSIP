import secrets
import string
import tkinter as tk
from tkinter import messagebox, ttk

import pyperclip

PASSWORD_PLACEHOLDER = "Generate a secure password to get started"
password_history = []


def calculate_strength(password):
    """Return a strength label and score from 1 to 4."""
    diversity = sum((any(c.isupper() for c in password), any(c.islower() for c in password), any(c.isdigit() for c in password), any(c in string.punctuation for c in password)))
    if len(password) >= 14 and diversity >= 3:
        return "Very strong", 4
    if len(password) >= 12 and diversity >= 3:
        return "Strong", 3
    if len(password) >= 10 and diversity >= 2:
        return "Medium", 2
    return "Weak", 1


def update_length(*_):
    try:
        value = max(8, min(64, int(length_var.get())))
    except (tk.TclError, ValueError):
        return
    length_var.set(value)
    length_hint.config(text=f"{value} characters")


def character_groups():
    options = ((uppercase_var.get(), string.ascii_uppercase), (lowercase_var.get(), string.ascii_lowercase), (numbers_var.get(), string.digits), (symbols_var.get(), string.punctuation))
    groups = []
    for selected, characters in options:
        if selected:
            groups.append("".join(c for c in characters if c not in "0Ol1") if ambiguous_var.get() else characters)
    return groups


def update_history(password):
    password_history.append(password)
    del password_history[:-5]
    history_list.configure(state="normal")
    history_list.delete("1.0", tk.END)
    for number, saved in enumerate(reversed(password_history), 1):
        history_list.insert(tk.END, f"{number}.  {saved}\n")
    history_list.configure(state="disabled")


def set_strength(password):
    label, score = calculate_strength(password)
    colors = {1: "#f87171", 2: "#fbbf24", 3: "#38bdf8", 4: "#4ade80"}
    strength_bar["value"] = score
    strength_text.config(text=label, foreground=colors[score])
    strength_detail.config(text=f"Security score: {score} / 4")


def generate_password():
    try:
        length = int(length_var.get())
    except (tk.TclError, ValueError):
        messagebox.showerror("Invalid length", "Enter a whole number between 8 and 64.")
        return
    if not 8 <= length <= 64:
        messagebox.showerror("Invalid length", "Choose a length between 8 and 64 characters.")
        return
    groups = character_groups()
    if len(groups) < 2:
        messagebox.showerror("Choose more types", "Select at least two character types.")
        return

    characters = [secrets.choice(group) for group in groups]
    pool = "".join(groups)
    characters.extend(secrets.choice(pool) for _ in range(length - len(groups)))
    secrets.SystemRandom().shuffle(characters)
    password = "".join(characters)
    password_var.set(password)
    password_output.config(show="" if show_password_var.get() else "•")
    copy_button.state(["!disabled"])
    copy_status.config(text="Ready to copy", foreground="#94a3b8")
    set_strength(password)
    update_history(password)


def copy_password():
    password = password_var.get()
    if not password or password == PASSWORD_PLACEHOLDER:
        messagebox.showwarning("No password", "Generate a password first.")
        return
    try:
        pyperclip.copy(password)
    except pyperclip.PyperclipException:
        root.clipboard_clear()
        root.clipboard_append(password)
    copy_status.config(text="Copied to clipboard", foreground="#4ade80")
    root.after(2500, lambda: copy_status.config(text="Ready to copy", foreground="#94a3b8"))


def toggle_password():
    if password_var.get() != PASSWORD_PLACEHOLDER:
        password_output.config(show="" if show_password_var.get() else "•")


def clear_history():
    password_history.clear()
    history_list.configure(state="normal")
    history_list.delete("1.0", tk.END)
    history_list.insert(tk.END, "No generated passwords yet.")
    history_list.configure(state="disabled")


root = tk.Tk()
root.title("Password Forge")
root.geometry("730x700")
root.minsize(650, 630)
root.configure(bg="#0f172a")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background="#0f172a")
style.configure("Card.TFrame", background="#18233a")
style.configure("Title.TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 24, "bold"))
style.configure("Sub.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 10))
style.configure("CardTitle.TLabel", background="#18233a", foreground="#f8fafc", font=("Segoe UI", 13, "bold"))
style.configure("Body.TLabel", background="#18233a", foreground="#cbd5e1", font=("Segoe UI", 10))
style.configure("TCheckbutton", background="#18233a", foreground="#e2e8f0", font=("Segoe UI", 10), focuscolor="#18233a")
style.map("TCheckbutton", background=[("active", "#18233a")], foreground=[("active", "#ffffff")])
style.configure("Accent.TButton", background="#6366f1", foreground="white", borderwidth=0, font=("Segoe UI", 11, "bold"), padding=(18, 11))
style.map("Accent.TButton", background=[("active", "#818cf8"), ("pressed", "#4f46e5")])
style.configure("Secondary.TButton", background="#283652", foreground="#e2e8f0", borderwidth=0, font=("Segoe UI", 10, "bold"), padding=(12, 8))
style.map("Secondary.TButton", background=[("active", "#364665")])
style.configure("Strength.Horizontal.TProgressbar", troughcolor="#26334d", background="#4ade80", bordercolor="#26334d", lightcolor="#4ade80", darkcolor="#4ade80")

length_var = tk.IntVar(value=16)
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
ambiguous_var = tk.BooleanVar(value=False)
show_password_var = tk.BooleanVar(value=True)
password_var = tk.StringVar(value=PASSWORD_PLACEHOLDER)

header = ttk.Frame(root)
header.pack(fill="x", padx=42, pady=(32, 20))
ttk.Label(header, text="Password Forge", style="Title.TLabel").pack(anchor="w")
ttk.Label(header, text="Create strong, unique passwords in a few clicks.", style="Sub.TLabel").pack(anchor="w", pady=(2, 0))

content = ttk.Frame(root)
content.pack(fill="both", expand=True, padx=42, pady=(0, 32))
content.columnconfigure((0, 1), weight=1)

settings = ttk.Frame(content, style="Card.TFrame", padding=24)
settings.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
ttk.Label(settings, text="Password settings", style="CardTitle.TLabel").pack(anchor="w")
length_row = ttk.Frame(settings, style="Card.TFrame")
length_row.pack(fill="x", pady=(22, 4))
ttk.Label(length_row, text="Length", style="Body.TLabel").pack(side="left")
length_hint = ttk.Label(length_row, text="16 characters", style="Body.TLabel")
length_hint.pack(side="right")
length_control = ttk.Frame(settings, style="Card.TFrame")
length_control.pack(fill="x")
ttk.Scale(length_control, from_=8, to=64, variable=length_var, command=update_length).pack(side="left", fill="x", expand=True, padx=(0, 14))
length_spin = ttk.Spinbox(length_control, from_=8, to=64, textvariable=length_var, width=5, justify="center")
length_spin.pack(side="right")
length_spin.bind("<FocusOut>", update_length)
length_spin.bind("<Return>", update_length)
ttk.Separator(settings).pack(fill="x", pady=20)
ttk.Label(settings, text="Include", style="CardTitle.TLabel").pack(anchor="w")
for text, variable in (("Uppercase letters  A–Z", uppercase_var), ("Lowercase letters  a–z", lowercase_var), ("Numbers  0–9", numbers_var), ("Symbols  ! @ # …", symbols_var)):
    ttk.Checkbutton(settings, text=text, variable=variable).pack(anchor="w", pady=5)
ttk.Separator(settings).pack(fill="x", pady=15)
ttk.Checkbutton(settings, text="Exclude ambiguous characters (0, O, l, 1)", variable=ambiguous_var).pack(anchor="w")
ttk.Button(settings, text="Generate secure password", style="Accent.TButton", command=generate_password).pack(fill="x", pady=(22, 0))

result = ttk.Frame(content, style="Card.TFrame", padding=24)
result.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
ttk.Label(result, text="Your new password", style="CardTitle.TLabel").pack(anchor="w")
ttk.Label(result, text="A cryptographically secure password, ready to use.", style="Body.TLabel").pack(anchor="w", pady=(4, 18))
password_output = tk.Entry(result, textvariable=password_var, state="readonly", readonlybackground="#101a2d", fg="#f8fafc", relief="flat", font=("Consolas", 12, "bold"), justify="center")
password_output.pack(fill="x", ipady=15)
actions = ttk.Frame(result, style="Card.TFrame")
actions.pack(fill="x", pady=(10, 18))
copy_button = ttk.Button(actions, text="Copy password", style="Secondary.TButton", command=copy_password, state="disabled")
copy_button.pack(side="left")
ttk.Checkbutton(actions, text="Show password", variable=show_password_var, command=toggle_password).pack(side="right")
copy_status = tk.Label(result, text="Generate a password first", bg="#18233a", fg="#94a3b8", font=("Segoe UI", 9))
copy_status.pack(anchor="w", pady=(0, 15))
strength_row = ttk.Frame(result, style="Card.TFrame")
strength_row.pack(fill="x")
ttk.Label(strength_row, text="Strength", style="Body.TLabel").pack(side="left")
strength_text = tk.Label(strength_row, text="Not generated", bg="#18233a", fg="#94a3b8", font=("Segoe UI", 10, "bold"))
strength_text.pack(side="right")
strength_bar = ttk.Progressbar(result, style="Strength.Horizontal.TProgressbar", maximum=4, value=0)
strength_bar.pack(fill="x", pady=(8, 5))
strength_detail = ttk.Label(result, text="Security score: —", style="Body.TLabel")
strength_detail.pack(anchor="w")

history = ttk.Frame(content, style="Card.TFrame", padding=20)
history.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(20, 0))
history_header = ttk.Frame(history, style="Card.TFrame")
history_header.pack(fill="x", pady=(0, 10))
ttk.Label(history_header, text="Recent passwords", style="CardTitle.TLabel").pack(side="left")
ttk.Button(history_header, text="Clear history", style="Secondary.TButton", command=clear_history).pack(side="right")
history_box = ttk.Frame(history, style="Card.TFrame")
history_box.pack(fill="both", expand=True)
history_list = tk.Text(history_box, height=5, bg="#101a2d", fg="#cbd5e1", relief="flat", font=("Consolas", 10), padx=14, pady=10, state="disabled")
history_scroll = ttk.Scrollbar(history_box, orient="vertical", command=history_list.yview)
history_list.configure(yscrollcommand=history_scroll.set)
history_list.pack(side="left", fill="both", expand=True)
history_scroll.pack(side="right", fill="y")
clear_history()

root.bind("<Control-g>", lambda event: generate_password())
root.bind("<Control-c>", lambda event: copy_password())
root.mainloop()
