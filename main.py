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
import time
from words import Words

window = Tk()
window.title("Typing Speed Test")
words = Words()

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
word_frame = LabelFrame(window, height=400, width=600)
word_frame.pack()

# Creates dictionary of words with their corresponding word labels.
word_labels = {}
for word in words.words_for_test[:5]:
    word_label = Label(word_frame, text=word)
    word_label.text = word
    word_labels[words.words_for_test.index(word)] = word_label
    word_label.pack()

word_counter = 0
current_word = word_labels[word_counter].text
letter_counter = 0
current_letter = list(current_word)[letter_counter]

def check_word():
    global current_word
    word_labels[word_counter].configure(bg="light green")

def new_word():
    global letter_counter, current_letter, current_word, word_counter
    text_entry.delete(0, END)
    word_labels[word_counter].configure(bg="light blue")
    word_counter += 1
    letter_counter = 0
    current_word = word_labels[word_counter].text
    current_letter = list(current_word)[letter_counter]
    word_labels[word_counter].configure(bg="light green")

def check_letter(event):
    global letter_counter, current_letter, current_word, word_counter
    if event.keysym == current_letter:
        print(f"CORRECT LETTER: {current_letter}")
        if letter_counter == len(current_word) - 1:
            new_word()
        else:
            letter_counter += 1
            current_letter = list(current_word)[letter_counter]
    elif event.keysym == "space":
        new_word()
    else:
        print(f"WRONG LETTER: {event.keysym}")

# Get the current word, and convert it into a list of characters.
# Find a way to use keyboard event listeners
# If the character entered is the same as the corresponding character in the list, then text = blue, else red
# When the user presses space, then it will go onto the next word. If any characters mismatch, then make the word red.


# Text box for user input
text_entry = Entry(window, text="Type here:")
text_entry.focus()
text_entry.pack()

check_word()

window.bind("<KeyPress>", check_letter)


window.mainloop()