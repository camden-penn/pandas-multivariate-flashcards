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
FILL_VOLUME = (tk.N,tk.S,tk.E,tk.W)

is_question_side = True

window = tk.Tk()
window.title('Flashcards')

card_front = tk.StringVar(window)
if DEBUG:
    card_front.trace('w', lambda x,y,z: print(card_front.get()))
card_back = tk.StringVar(window)
if DEBUG:
    card_back.trace('w', lambda x,y,z: print(card_back.get()))

flashcard = tk.Label(text='Initializing...', font=FLASHCARD_FONT)
flashcard.grid(columnspan=4, rowspan=3)

def deconstruct_elements(elements):
    for element in elements:
        element.destroy()

def window_transition(old_scene_elements, new_scene_handle):
    deconstruct_elements(old_scene_elements)
    new_scene_handle()

def begin_flashcards():
    print("test")

def init_flashcard_set():
    flashcard['text'] = "Choose the flashcards'\n front and back."
    flashcard_settings = tk.Frame(window)
    flashcard_settings['bg']='yellow'
    flashcard_settings.grid(columnspan=4,sticky=FILL_VOLUME)
    for row in range(0,2):
        flashcard_settings.grid_rowconfigure(row, weight=1)
    for col in range(0, 4):
        flashcard_settings.grid_columnconfigure(col, weight=1)

    card_front_label = tk.Label(flashcard_settings, text="Front: ", font=MINOR_FONT)
    card_front_label.grid(row=0, column=0, sticky=FILL_VOLUME)

    card_front_dropdown = tk.OptionMenu(flashcard_settings, card_front, *data_columns)
    card_front_dropdown.config(font=MINOR_FONT)
    # Yes, the font for the dropdown includes the window, _TKINTER_. What's wrong with you?!
    flashcard_settings.nametowidget(card_front_dropdown.menuname).config(font=MINOR_FONT)
    card_front.set(data_columns[0])
    card_front_dropdown.grid(row=0, column=1)

    card_back_label = tk.Label(flashcard_settings, text="Back: ", font=MINOR_FONT)
    card_back_label.grid(row=0, column=2, sticky=FILL_VOLUME)

    card_back_dropdown = tk.OptionMenu(flashcard_settings, card_back, *data_columns)
    card_back_dropdown.config(font=MINOR_FONT)
    flashcard_settings.nametowidget(card_back_dropdown.menuname).config(font=MINOR_FONT)
    card_back.set(data_columns[1])
    card_back_dropdown.grid(row=0, column=3)

    done_button = tk.Button(flashcard_settings, text="Done", font=MINOR_FONT)
    done_button.grid(row=1, column=2, columnspan=2, sticky=FILL_VOLUME)

    done_button['command'] = lambda:window_transition([flashcard_settings], begin_flashcards)

init_flashcard_set()

window.mainloop()



