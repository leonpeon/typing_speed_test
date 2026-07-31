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
words = Words()

word_font = tkFont.Font(
    family="Arial",
    size=36,
    weight=tkFont.NORMAL
)


# Adjusts placement of window
window_width = 900
window_height = 400
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - screen_height) // 2 + 25
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Title of program
title_label = Label(window, text="TYPING SPEED TEST")
title_label.pack()

# Word display frame
word_frame = LabelFrame(window, height=600, width=800)
word_frame.pack()
word_frame.pack_propagate(False)

# Creates dictionary of words with their corresponding word labels.
word_labels = []
for word in words.words_for_test[:15]:
    word_label = Label(word_frame, text=word, font=word_font)
    word_label.text = word
    word_labels.append(word_label)

row = 0
column = 0
for word in word_labels:
    if column == 5:
        row += 1
        column = 0
    word.grid(column=column, row=row)
    column += 1

word_counter = 0
current_word = word_labels[word_counter].text
letter_counter = 0
current_letter = list(current_word)[letter_counter]
user_inputs = []

# Provides the first word
def check_word():
    global current_word
    word_labels[word_counter].configure(bg="light blue")

# Provides a new word everytime the user presses space
def new_word():
    global letter_counter, current_letter, current_word, word_counter, user_inputs
    text_entry.delete(0, END)
    word_counter += 1
    letter_counter = 0
    current_word = word_labels[word_counter].text
    current_letter = list(current_word)[letter_counter]
    word_labels[word_counter].configure(bg="light blue")
    user_inputs = []
    

# Checks if the user input matches the correct letter.
def check_letter(event):
    global letter_counter, current_letter, current_word, user_inputs

    if event.keysym == "BackSpace":
        if user_inputs:
            user_inputs.pop()

    elif event.keysym == "space":
            print(user_inputs)
            print(list(current_word))
    
            if user_inputs == list(current_word):
                word_labels[word_counter].configure(bg="light green")
    
            else:
                word_labels[word_counter].configure(bg="red")
            new_word()

    elif event.keysym == current_letter:
        print(f"CORRECT LETTER: {current_letter}")
        user_inputs.append(event.char)
        if letter_counter >= len(current_word) - 1:
            pass
        else:
            letter_counter += 1
            current_letter = list(current_word)[letter_counter]

    elif event.char in ["\r", "", "\t"]:
        pass

    else:
        user_inputs.append(event.char)
        print(f"WRONG LETTER: {event.keysym}")


# Text box for user input
text_entry = Entry(window, text="Type here:")
text_entry.focus()
text_entry.pack()

check_word()

text_entry.bind("<KeyPress>", check_letter)


window.mainloop()