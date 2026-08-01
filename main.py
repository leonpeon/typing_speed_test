import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from words import Words

window = Tk()
window.title("Typing Speed Test")
window.resizable(False, False)
words = Words()
time_left = 61
with open("highest_wpm.txt") as file:
    high_score = float(file.readline())
can_type = False # If false, keypresses will not modify the words

TITLE_FONT = tkFont.Font(
    family="Segoe UI",
    size=44,
    weight="bold"
)

WORD_FONT = tkFont.Font(
    family="Arial",
    size=36,
    weight=tkFont.NORMAL
)

LABEL_FONT = tkFont.Font(
    family="Consolas",
    size=20,
    weight="normal"
)

BG_COLOUR = "pink"

# Title of program
title_label = Label(window, text="TYPING SPEED TEST", font=TITLE_FONT, fg="purple", bg=BG_COLOUR)
title_label.pack()

# Word display frame
canvas_container = LabelFrame(window)
canvas_frame = Canvas(canvas_container, height=234, width=850)
word_frame = Frame(canvas_frame)
canvas_frame.create_window((0,0), window=word_frame, anchor="nw")
canvas_container.pack()
canvas_frame.pack()

word_frame.bind(
    "<Configure>",
    lambda e: canvas_frame.configure(
        scrollregion=canvas_frame.bbox("all")
    )
)

word_units = {} # A frame which contains the labels of each letter of each word.
word_dict = {}

# Creates the display and dictionary of words with their corresponding word labels.
def word_bank():
    global word_units, word_dict
    word_units = {}
    row = 0
    column = 0
    for word in words.words_for_test:
        word_unit = Frame(word_frame, width=160, height=150)

        letter_labels = []
        for letter in list(word):
            letter_label = Label(word_unit, text=letter, font=WORD_FONT, pady=10)
            letter_labels.append(letter_label)
            letter_label.pack(side="left")

        word_units[word] = [word_unit, letter_labels] # Dictionary is {word: [word_frame, list of letter frames]}

        if column == 5:
            row += 1
            column = 0
        word_unit.grid(column=column, row=row)
        column += 1

        word_dict = list(word_units.keys())

word_bank()

# Provides the first word
def check_word():
    global current_word, current_letter_list
    for letter in current_letter_list:
        letter.configure(bg="light blue")

# Refreshs the letter / word everytime the user makes a keypress
def refresh_word():
    global word_counter, current_word, current_letter_list, letter_counter, current_letter, user_inputs
    current_word = word_dict[word_counter]
    current_letter_list = word_units[current_word][1]
    try:
        current_letter = list(current_word)[letter_counter]
    except IndexError:
        current_letter = None

# Provides a new word everytime the user presses space
def new_word():
    global letter_counter, word_counter, user_inputs, current_letter_list
    text_entry.delete(0, END)
    word_counter += 1
    letter_counter = 0
    refresh_word()
    for letter in current_letter_list:
        letter.configure(bg="light blue")

    if word_counter + 1 >= 11 and word_counter % 5 == 0:
        scroll_down()
    user_inputs = []
    
# Checks if the user input matches the correct letter.
def check_letter(event):
    global letter_counter, current_letter, current_word, user_inputs, current_letter_list, correct_characters, incorrect_characters, can_type
    if not can_type:
        pass
    else:
        if event.keysym == "BackSpace":
            if user_inputs:
                user_inputs.pop()

                if len(current_letter_list) > len(current_word):
                    word_units[current_word][1].pop().destroy()

                elif letter_counter > 0:
                    letter_counter -= 1
                    refresh_word()
                    current_letter_list[letter_counter].config(bg="light blue")

        elif event.keysym == "space":
            for correct, typed in zip(current_word, user_inputs):
                if correct == typed:
                    correct_characters += 1
                else:
                    incorrect_characters += 1

            if len(user_inputs) < len(current_word):
                incorrect_characters += len(current_word) - len(user_inputs)
            elif len(user_inputs) > len(current_word):
                incorrect_characters += len(user_inputs) - len(current_word)

            new_word()

        elif event.char in ["\r", "", "\t"]:
                pass

        elif letter_counter > len(current_word) - 1:
            wrong_letters_add = Label(word_units[current_word][0], text=event.char, bg="red", font=WORD_FONT)
            user_inputs.append(event.char)
            word_units[current_word][1].append(wrong_letters_add)
            wrong_letters_add.pack(side="left")

        elif event.keysym == current_letter:
            user_inputs.append(event.char)
            current_letter_list[letter_counter].config(bg="light green")
            letter_counter += 1
            refresh_word()

        else:
            user_inputs.append(event.char)
            current_letter_list[letter_counter].config(bg="red")
            letter_counter += 1
            refresh_word()

def scroll_down():
    global move_units
    move_units += 0.025
    canvas_frame.yview_moveto(move_units)

def start_timer():
    global time_left, can_type
    words.test_words()
    score_label.config(text=f"Score: --")
    if time_left > 0:
        start_button.config(text="Restart", command=end_timer)
        text_entry.config(state="normal")
        can_type = True

        time_left -= 1
        timer_label.config(text=f"Timer: {time_left}")
        window.after(1000, start_timer)

    elif time_left == 0:
        words_per_minute()
        reset()
        time_left = 61

def end_timer():
    global time_left
    time_left = 0
    reset()

def reset():
    global word_units, letter_counter, word_counter, user_inputs, can_type
    for label, _ in word_units.values():
            label.destroy()

    word_units = {}
    letter_counter = 0 
    word_counter = 0 
    user_inputs = [] 
    can_type = False 
    text_entry.delete(0, END)
    timer_label.config(text=f"Timer: --")
    text_entry.config(state="disabled")
    start_button.config(text="Start", command=start_timer)
    words.test_words()
    word_bank()
    refresh_word()
    canvas_frame.yview_moveto(0)

def words_per_minute():
    global correct_characters, incorrect_characters
    total_characters = correct_characters + incorrect_characters
    raw_wpm = (total_characters/5)
    try:
        accuracy = (correct_characters/total_characters) * 100
    except ZeroDivisionError:
        accuracy = 0
    adjusted_wpm = raw_wpm * (accuracy/100)
    score_label.config(text=f"WPM: {adjusted_wpm:.1f}")
    with open("highest_wpm.txt", "r+") as file:
        highest_wpm = float(file.read())

        if adjusted_wpm > highest_wpm:
            high_score_label.config(text=f"WPM: {adjusted_wpm:.1f}")
            file.seek(0)
            file.write(f"{adjusted_wpm:.1f}")
            file.truncate()
    
    correct_characters = 0
    incorrect_characters = 0

word_frame.update_idletasks()
canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))

# Main variables
word_counter = 0 # Tracks index of current word within word list
current_word = word_dict[word_counter] # Tracks current word
current_letter_list = word_units[current_word][1] # List of letters within the current word
letter_counter = 0 # Tracks index of current letter within the word
current_letter = list(current_word)[letter_counter] # Current letter of current word
user_inputs = [] # Tracks the keypresses the user makes
move_units = 0 # Tracks where the position of the user's screen
correct_characters = 0 # Tracks the amount of correct characters the user typed
incorrect_characters = 0 # Tracks the amount of incorrect characters

# Adjusts placement of window
window_width = 1000
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - screen_height) // 2 + 25
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.config(bg=BG_COLOUR)

# Text box for user input
bottom_frame = Frame(window, bg=BG_COLOUR)
bottom_frame.pack()
text_entry = Entry(bottom_frame, text="Type here:", state="disabled", font=("arial", 24), bg="light yellow")
text_entry.focus()
text_entry.grid(column=1, row=0, padx=30, pady=10)
timer_label = Label(bottom_frame, text=f"Timer: --", font=LABEL_FONT, bg=BG_COLOUR)
timer_label.grid(column=0, row=0)
score_label = Label(bottom_frame, text=f"Score: --", font=LABEL_FONT, bg=BG_COLOUR)
score_label.grid(column=2, row=0)
high_score_label = Label(bottom_frame, text=f"Highest WPM: {high_score}", font=LABEL_FONT, bg=BG_COLOUR)
high_score_label.grid(column=2, row=1)
start_button = Button(bottom_frame, text="Start", font=("arial", 14), command=start_timer)
start_button.grid(column=1, row=1, pady=20)

check_word()
text_entry.bind("<KeyPress>", check_letter)

window.mainloop()