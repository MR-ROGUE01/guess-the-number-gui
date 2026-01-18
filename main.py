"""
Guess The Number Game
A Python GUI game built using Tkinter.
Focus: event-driven design, clean UI, and state management.
"""

import tkinter as tk
from tkinter import messagebox
import random

# ================= WINDOW =================
root = tk.Tk()
root.title("Guess The Number 🎮 | Python GUI")
root.geometry("460x640")
root.resizable(False, False)

# ================= BACKGROUND CANVAS =================
canvas = tk.Canvas(root, width=460, height=640, bg="#0B061F", highlightthickness=0)
canvas.place(x=0, y=0)

def draw_graffiti():
    colors = ["#9B5CFF", "#FF4ECD", "#4DD0FF", "#FFD84D"]

    # Abstract blobs
    for _ in range(6):
        x1 = random.randint(-150, 300)
        y1 = random.randint(-150, 450)
        x2 = x1 + random.randint(250, 450)
        y2 = y1 + random.randint(250, 450)
        canvas.create_oval(
            x1, y1, x2, y2,
            fill=random.choice(colors),
            outline="",
            stipple="gray25"
        )

    # Neon circles
    for _ in range(16):
        x = random.randint(0, 460)
        y = random.randint(0, 640)
        r = random.randint(8, 22)
        canvas.create_oval(
            x-r, y-r, x+r, y+r,
            outline=random.choice(colors),
            width=2
        )

draw_graffiti()

# ================= MAIN CARD =================
card = tk.Frame(root, bg="#1A1238")
card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=540)

# ================= GAME STATE =================
low = 0
high = 0
mid = 0
attempts = 0

# ================= UI =================
title = tk.Label(
    card,
    text="🧠 GUESS THE NUMBER",
    font=("Segoe UI", 20, "bold"),
    fg="#EDEAFF",
    bg="#1A1238"
)
title.pack(pady=15)

info = tk.Label(
    card,
    text="Set a range and let the computer guess",
    font=("Segoe UI", 11),
    fg="#9B8CFF",
    bg="#1A1238"
)
info.pack(pady=5)

# ===== RANGE INPUT =====
range_frame = tk.Frame(card, bg="#1A1238")
range_frame.pack(pady=10)

def create_entry(parent, label):
    frame = tk.Frame(parent, bg="#1A1238")
    frame.pack(side="left", padx=15)
    tk.Label(frame, text=label, fg="#EDEAFF", bg="#1A1238").pack()
    entry = tk.Entry(frame, width=8, font=("Segoe UI", 12), justify="center")
    entry.pack(pady=5)
    return entry

start_entry = create_entry(range_frame, "START")
end_entry = create_entry(range_frame, "END")

# ===== START BUTTON =====
start_btn = tk.Button(
    card,
    text="🚀 START GAME",
    font=("Segoe UI", 12, "bold"),
    bg="#9B5CFF",
    fg="white",
    bd=0,
    padx=20,
    pady=8
)
start_btn.pack(pady=20)

# ===== GUESS DISPLAY =====
guess_label = tk.Label(
    card,
    text="",
    font=("Segoe UI", 18, "bold"),
    fg="#FFD84D",
    bg="#1A1238"
)
guess_label.pack(pady=20)

attempt_label = tk.Label(
    card,
    text="Attempts: 0",
    font=("Segoe UI", 11),
    fg="#4DD0FF",
    bg="#1A1238"
)
attempt_label.pack()

# ===== ACTION BUTTONS =====
btn_frame = tk.Frame(card, bg="#1A1238")
btn_frame.pack(pady=20)

def game_button(parent, text, color, cmd):
    return tk.Button(
        parent,
        text=text,
        width=12,
        font=("Segoe UI", 10, "bold"),
        bg=color,
        fg="#000000",
        bd=0,
        pady=6,
        state=tk.DISABLED,
        command=cmd
    )

YES_COLOR  = "#A7E3D0"   # confirm
HIGH_COLOR = "#AFCBFF"   # higher
LOW_COLOR  = "#F4B6B6"   # lower

yes_btn = game_button(btn_frame, "✅ CONFIRM", YES_COLOR, lambda: correct())
high_btn = game_button(btn_frame, "⬆ HIGHER", HIGH_COLOR, lambda: higher())
low_btn = game_button(btn_frame, "⬇ LOWER", LOW_COLOR, lambda: lower())

yes_btn.pack(side="left", padx=6)
high_btn.pack(side="left", padx=6)
low_btn.pack(side="left", padx=6)

# ===== RESTART =====
restart_btn = tk.Button(
    card,
    text="🔁 RESTART",
    font=("Segoe UI", 11, "bold"),
    bg="#2C2159",
    fg="white",
    bd=0,
    state=tk.DISABLED
)
restart_btn.pack(pady=10)

# ================= GAME LOGIC =================
def start_game():
    global low, high, attempts
    try:
        low = int(start_entry.get())
        high = int(end_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")
        return

    if low > high:
        messagebox.showerror("Error", "Start must be less than or equal to End.")
        return

    attempts = 0
    enable_buttons()
    next_guess()

def next_guess():
    global mid, attempts
    if low > high:
        guess_label.config(text="Inconsistent answers detected!")
        end_game()
        return

    mid = (low + high) // 2
    attempts += 1
    guess_label.config(text=f"Is it {mid}?")
    attempt_label.config(text=f"Attempts: {attempts}")

def correct():
    guess_label.config(text=f"🎉 Guessed in {attempts} attempts!")
    end_game()

def higher():
    global low
    low = mid + 1
    next_guess()

def lower():
    global high
    high = mid - 1
    next_guess()

def end_game():
    disable_buttons()
    restart_btn.config(state=tk.NORMAL)

def reset_game():
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)
    guess_label.config(text="")
    attempt_label.config(text="Attempts: 0")
    restart_btn.config(state=tk.DISABLED)

def enable_buttons():
    yes_btn.config(state=tk.NORMAL)
    high_btn.config(state=tk.NORMAL)
    low_btn.config(state=tk.NORMAL)

def disable_buttons():
    yes_btn.config(state=tk.DISABLED)
    high_btn.config(state=tk.DISABLED)
    low_btn.config(state=tk.DISABLED)

# ================= BIND =================
start_btn.config(command=start_game)
restart_btn.config(command=reset_game)

# ================= RUN =================
root.mainloop()
