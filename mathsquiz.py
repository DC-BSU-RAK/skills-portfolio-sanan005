#calling out the tk functions
import tkinter as tk
from tkinter import messagebox
import random

#begining the main code
root = tk.Tk()
root.title("Math Quiz")

# listing variables
score = 0
question_count = 0
min_num = 0
max_num = 0
a = 0
b = 0
operation = ''
correct_answer = 0
attempt = 0

# Widgets
label = None
entry = None
button = None


def displayMenu():
    clear_screen()
    tk.Label(root, text="DIFFICULTY LEVEL\n1. Easy\n2. Moderate\n3. Advanced", font=("Arial", 12)).pack(pady=20)
    tk.Button(root, text="1. Easy", width=15, command=lambda: start_quiz(1)).pack(pady=5)
    tk.Button(root, text="2. Moderate", width=15, command=lambda: start_quiz(2)).pack(pady=5)
    tk.Button(root, text="3. Advanced", width=15, command=lambda: start_quiz(3)).pack(pady=5)

def randomInt():
    global min_num, max_num
    return random.randint(min_num, max_num)

def decideOperation():
    return random.choice(['+', '-'])

def displayProblem():
    global label, entry, button, a, b, operation
    clear_screen()
    label = tk.Label(root, text=f"Question {question_count}/10:\n\n{a} {operation} {b} =", font=("Arial", 14))
    label.pack(pady=20)
    entry = tk.Entry(root, font=("Arial", 12), width=10, justify='center')
    entry.pack(pady=10)
    entry.focus()
    button = tk.Button(root, text="Submit", command=submit_answer)
    button.pack(pady=10)

def isCorrect(user_answer):
    global correct_answer, attempt
    if user_answer == correct_answer:
        if attempt == 0:
            messagebox.showinfo("Correct!", "Great job!")
        else:
            messagebox.showinfo("Correct!", "Good, on second try!")
        return True
    else:
        if attempt == 0:
            messagebox.showwarning("Wrong", "Try again!")
        else:
            messagebox.showerror("Wrong", f"Correct answer was {correct_answer}")
        return False

def displayResults():
    clear_screen()
    rank = "F"
    if score >= 90:
        rank = "A+"
    elif score >= 80:
        rank = "A"
    elif score >= 70:
        rank = "B"
    elif score >= 60:
        rank = "C"

    result_text = f"Quiz Complete!\n\nScore: {score}/100\nGrade: {rank}"
    tk.Label(root, text=result_text, font=("Arial", 14)).pack(pady=30)
    tk.Button(root, text="Play Again", command=displayMenu).pack(pady=10)
    tk.Button(root, text="Quit", command=root.quit).pack(pady=5)


def start_quiz(level):
    global min_num, max_num, score, question_count
    if level == 1:
        min_num, max_num = 1, 9
    elif level == 2:
        min_num, max_num = 10, 99
    else:
        min_num, max_num = 1000, 9999
    score = 0
    question_count = 0
    next_question()

def next_question():
    global question_count, a, b, operation, correct_answer, attempt
    question_count += 1
    if question_count > 10:
        displayResults()
        return
    attempt = 0
    a = randomInt()
    b = randomInt()
    operation = decideOperation()
    if operation == '+':
        correct_answer = a + b
    else:
        if a < b:
            a, b = b, a  #  avoid negative
        correct_answer = a - b
    displayProblem()

def submit_answer():
    global score, attempt
    try:
        answer = int(entry.get())
    except:
        messagebox.showerror("Error", "Please enter a number!")
        return

    if isCorrect(answer):
        if attempt == 0:
            score += 10
        else:
            score += 5
        next_question()
    else:
        if attempt == 0:
            attempt = 1
            entry.delete(0, tk.END)
        else:
            next_question()

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

displayMenu()
root.mainloop()
