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
can_type = False

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

# Title of program
title_label = Label(window, text="TYPING SPEED TEST", font=TITLE_FONT, fg="purple")
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

# Creates dictionary of words with their corresponding word labels.
word_units = {} # A frame which contains the labels of each letter of each word.
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

word_frame.update_idletasks()
canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))

word_counter = 0
current_word = word_dict[word_counter]
current_letter_list = word_units[current_word][1]
letter_counter = 0
current_letter = list(current_word)[letter_counter]
user_inputs = []
move_units = 0

correct_characters = 0
incorrect_characters = 0

# Refreshs the letter / word everytime the user makes a keypress
def refresh_word():
    global word_counter, current_word, current_letter_list, letter_counter, current_letter, user_inputs
    current_word = word_dict[word_counter]
    current_letter_list = word_units[current_word][1]
    try:
        current_letter = list(current_word)[letter_counter]
    except IndexError:
        current_letter = None

# Provides the first word
def check_word():
    global current_word, current_letter_list
    for letter in current_letter_list:
        letter.configure(bg="light blue")

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
            print(f"CORRECT LETTER: {current_letter}")
            user_inputs.append(event.char)
            current_letter_list[letter_counter].config(bg="light green")
            letter_counter += 1
            refresh_word()

        else:
            user_inputs.append(event.char)
            current_letter_list[letter_counter].config(bg="red")
            letter_counter += 1
            print(f"WRONG LETTER: {event.keysym}")
            refresh_word()

def scroll_down():
    global move_units
    move_units += 0.025
    canvas_frame.yview_moveto(move_units)

def start_timer():
    global time_left, can_type
    if time_left > 0:
        start_button.config(text="Stop", command=end_timer)
        text_entry.config(state="normal")
        can_type = True

        time_left -= 1
        timer_label.config(text=f"Timer: {time_left}")
        window.after(1000, start_timer)

    elif time_left == 0:
        words_per_minute()
        text_entry.config(state="disabled")
        can_type = False
        time_left = 61

def end_timer():
    global time_left
    time_left = 0
    start_button.config(text="Start", command=start_timer)

def words_per_minute():
    global correct_characters, incorrect_characters
    total_characters = correct_characters + incorrect_characters
    raw_wpm = (total_characters/5)
    accuracy = (correct_characters/total_characters) * 100
    adjusted_wpm = raw_wpm * (accuracy/100)
    score_label.config(text=f"WPM: {adjusted_wpm:.1f}")
    with open("highest_wpm.txt", "w") as file:
        file.write(f"{adjusted_wpm:.1f}")
    
    correct_characters = 0
    incorrect_characters = 0

# Text box for user input
bottom_frame = Frame(window)
bottom_frame.pack()
text_entry = Entry(bottom_frame, text="Type here:", state="disabled")
text_entry.focus()
text_entry.grid(column=1, row=0, padx=30, pady=10)
timer_label = Label(bottom_frame, text=f"Timer: --", font=LABEL_FONT)
timer_label.grid(column=0, row=0)
score_label = Label(bottom_frame, text=f"WPM: {high_score}", font=LABEL_FONT)
score_label.grid(column=2, row=0)
start_button = Button(bottom_frame, text="Start", command=start_timer)
start_button.grid(column=1, row=1, pady=20)


check_word()

text_entry.bind("<KeyPress>", check_letter)


# Adjusts placement of window
window_width = 1000
window_height = 600
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - screen_height) // 2 + 25
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.mainloop()