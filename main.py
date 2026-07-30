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
window_height = 600
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

for word in words.words_for_test[:5]:
    word_label = Label(word_frame, text=word)
    word_label.pack() 

# Text box for user input
text_entry = Entry(window, text="Type here:")
text_entry.focus()
text_entry.pack()


window.mainloop()