import os
import pandas as pd
import tkinter as tk
import exceptions as oops

flashcard_data = pd.read_csv('防振りの単語.csv')
data_columns = flashcard_data.dtypes.index
if len(data_columns) < 2:
    raise oops.NotEnoughColumns

DEBUG = True
FLASHCARD_FONT = ('Helvetica', 40)
MINOR_FONT = ('Helvetica', 20)

is_question_side = True

window = tk.Tk()

card_front = tk.StringVar(window)
if DEBUG:
    card_front.trace('w', lambda x,y,z: print(card_front.get()))
card_back = tk.StringVar(window)
if DEBUG:
    card_back.trace('w', lambda x,y,z: print(card_back.get()))

flashcard = tk.Label(text='Initializing...', font=FLASHCARD_FONT)
flashcard.grid(columnspan=4, rowspan=3)

def init_flashcard_set():
    flashcard['text'] = "Choose the flashcards'\n front and back."

    card_front_label = tk.Label(window, text="Front: ", font=MINOR_FONT)
    card_front_label.grid(row=3, column=0)

    card_front_dropdown = tk.OptionMenu(window, card_front, *data_columns)
    card_front_dropdown.config(font=MINOR_FONT)
    # Yes, the font for the dropdown includes the window, _TKINTER_. What's wrong with you?!
    window.nametowidget(card_front_dropdown.menuname).config(font=MINOR_FONT)
    card_front.set(data_columns[0])
    card_front_dropdown.grid(row=3, column=1)

    card_back_label = tk.Label(window, text="Back: ", font=MINOR_FONT)
    card_back_label.grid(row=3, column=2)

    card_back_dropdown = tk.OptionMenu(window, card_back, *data_columns)
    card_back_dropdown.config(font=MINOR_FONT)
    window.nametowidget(card_back_dropdown.menuname).config(font=MINOR_FONT)
    card_back.set(data_columns[1])
    card_back_dropdown.grid(row=3, column=3)

    done_button = tk.Button(window, text="Done", command=deconstruct_elements())
    done_button.grid(row=4, column=2, columnspan=2)

init_flashcard_set()

window.mainloop()



