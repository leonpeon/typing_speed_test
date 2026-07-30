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

tk = Tk()

