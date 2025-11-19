import tkinter as tk
import random
import os

#
#joke path and codes
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "resources", "randomJokes.txt")

#all jokes relayed here
jokes = []
default_jokes = [
    ("Why did the scarecrow win an award?", "Because he was outstanding in his field."),
    ("Why don't scientists trust atoms?", "Because they make up everything."),
    ("Why did the math book look sad?", "Because it had too many problems."),
]

try:
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "?" not in line:
                continue

            # stripping optional part
            line = line.lstrip("- ").lstrip("-").strip()

            # Splitting
            parts = line.split("?", 1)
            if len(parts) != 2:
                continue

            setup = parts[0].strip() + "?"
            punchline = parts[1].strip()

            # Capitalize the punchline 
            if punchline:
                punchline = punchline[0].upper() + punchline[1:]

            jokes.append((setup, punchline))
except FileNotFoundError:
    jokes = []

# fall back to a small set of built-in jokes 
if not jokes:
    jokes = default_jokes.copy()
    using_fallback = True
else:
    using_fallback = False

# GUI Setup
root = tk.Tk()
root.title("Alexa Joke Assistant")
root.geometry("700x550")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

current_joke = None

# Title
title_label = tk.Label(
    root,
    text="🤖 Alexa, tell me a joke!",
    font=("Segoe UI", 24, "bold"),
    bg="#1e1e1e",
    fg="#00ff00"
)
title_label.pack(pady=(40, 20))

# Setup label
setup_label = tk.Label(
    root,
    text='Click the button below to hear a joke!',
    font=("Arial", 18),
    bg="#1e1e1e",
    fg="white",
    wraplength=650,
    justify="center"
)
setup_label.pack(pady=20)

# Punchline label (initially hidden)
punchline_label = tk.Label(
    root,
    text="",
    font=("Arial", 20, "italic"),
    bg="#1e1e1e",
    fg="#ff4444",
    wraplength=650,
    justify="center"
)
punchline_label.pack(pady=(0, 40))

def load_new_joke():
    global current_joke
    if not jokes:
        setup_label.config(text="⚠️ No jokes found in randomJokes.txt!", fg="#ff4444")
        punchline_label.config(text="")
        show_punchline_btn.config(state="disabled")
        return
    
    current_joke = random.choice(jokes)
    setup_label.config(text=current_joke[0], fg="white")
    punchline_label.config(text="")
    show_punchline_btn.config(state="normal")

def show_punchline():
    if current_joke:
        punchline_label.config(text=current_joke[1])

# Button frame
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=20)

# Alexa button
alexa_btn = tk.Button(
    btn_frame,
    text="Alexa tell me a Joke",
    font=("Helvetica", 16, "bold"),
    bg="#00bcd4",
    fg="white",
    activebackground="#0097a7",
    width=22,
    height=2,
    command=load_new_joke
)
alexa_btn.grid(row=0, column=0, padx=15)

# Show punchline button
show_punchline_btn = tk.Button(
    btn_frame,
    text="Show Punchline",
    font=("Helvetica", 14),
    bg="#ff9800",
    fg="white",
    activebackground="#f57c00",
    width=20,
    height=2,
    command=show_punchline,
    state="disabled"
)
show_punchline_btn.grid(row=0, column=1, padx=15)

# Next joke button
next_btn = tk.Button(
    btn_frame,
    text="Next Joke",
    font=("Helvetica", 14),
    bg="#4caf50",
    fg="white",
    activebackground="#388e3c",
    width=20,
    height=2,
    command=load_new_joke
)
next_btn.grid(row=1, column=0, pady=15)

# Quit button
quit_btn = tk.Button(
    btn_frame,
    text="Quit",
    font=("Helvetica", 14),
    bg="#f44336",
    fg="white",
    activebackground="#d32f2f",
    width=15,
    height=2,
    command=root.destroy
)
quit_btn.grid(row=1, column=1, pady=15)

root.mainloop()
