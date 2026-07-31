# TO DO:
# 1. Get a word list, which the computer will randomly select 150
# 2. Develop the basic GUI (each is a class): window, display text, text input, start button, timer, score
# 3. Find a way to change the colour of the text once the user types it out
# 4. Make the timer functional
# 5. Count the total of the user's correct/mistyped words, then calculate the score.
# 6. Store score into a text file

# CLASSES:
# Text: Displays text, changes text colour (depending on it was written correctly or not), 
#       highlights text, does not allow the user to type if the timer is not active.
# Button: Starts the timer, allows the user to type in text.
# Timer: One minute timer
# Score: Calculates WPM. Stores the score into a text file that can be referenced later.

import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import time
from words import Words

window = Tk()
window.title("Typing Speed Test")
window.resizable(False, False)
words = Words()

title_font = tkFont.Font(
    family="Segoe UI",
    size=44,
    weight="bold"
)

word_font = tkFont.Font(
    family="Arial",
    size=36,
    weight=tkFont.NORMAL
)

# Title of program
title_label = Label(window, text="TYPING SPEED TEST", font=title_font, fg="purple")
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
        letter_label = Label(word_unit, text=letter, font=word_font, pady=10)
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
    global letter_counter, current_letter, current_word, word_counter, user_inputs, current_letter_list
    text_entry.delete(0, END)
    word_counter += 1
    letter_counter = 0
    refresh_word()
    for letter in current_letter_list:
        letter.configure(bg="light blue")

    if word_counter + 1 >= 10 and (word_counter + 1) % 5 == 0:
        scroll_down()
    user_inputs = []
    
# Checks if the user input matches the correct letter.
def check_letter(event):
    global letter_counter, current_letter, current_word, user_inputs, current_letter_list

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
        new_word()

    elif event.char in ["\r", "", "\t"]:
            pass

    elif letter_counter > len(current_word) - 1:
        wrong_letters_add = Label(word_units[current_word][0], text=event.char, bg="red", font=word_font)
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

# Text box for user input
text_entry = Entry(window, text="Type here:")
text_entry.focus()
text_entry.pack()

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

# TO DO
# - Find a way to make the words scroll once the user has finished a line.
# - Create a timer and score system.