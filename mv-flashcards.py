import os
import pandas as pd
import tkinter as tk
import exceptions as oops
import random

flashcard_data = pd.read_csv('防振りの単語.csv')
data_columns = flashcard_data.dtypes.index
if len(data_columns) < 2:
    raise oops.NotEnoughColumns

DEBUG = True
FLASHCARD_FONT = ('Helvetica', 40)
MINOR_FONT = ('Helvetica', 20)
FILL_VOLUME = (tk.N,tk.S,tk.E,tk.W)

window = tk.Tk()
window.title('Flashcards')
window.geometry("600x420")
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

card_front = tk.StringVar(window)
if DEBUG:
    card_front.trace('w', lambda x,y,z: print(card_front.get()))
card_back = tk.StringVar(window)
if DEBUG:
    card_back.trace('w', lambda x,y,z: print(card_back.get()))

flashcard = tk.Label(text='Initializing...', font=FLASHCARD_FONT, wraplength=500)
flashcard.grid(sticky=FILL_VOLUME)

def deconstruct_elements(elements):
    for element in elements:
        element.destroy()

def window_transition(old_scene_elements, new_scene_handle):
    deconstruct_elements(old_scene_elements)
    new_scene_handle()

def advance_flashcard(card_set_data, card_order, curr_card_info, card_label, l_button, r_button, l_button_place_handle, go_back=False):
    curr_card_info['is_question_side'] = not curr_card_info['is_question_side']
    if go_back:
        curr_card_info['card_num'] = curr_card_info['card_num'] - 1
    if DEBUG:
        print(curr_card_info)
    if curr_card_info['is_question_side']:
        # Go to next card.
        if DEBUG:
            print("New question.")
        curr_card_info['card_num'] = (curr_card_info['card_num'] + 1)
        if curr_card_info['card_num'] >= len(card_order):
            # Starting over.
            curr_card_info['card_num'] = 0
            random.shuffle(card_order)
        # Display question side.
        r_button['text']="Show"
        card_label['text'] = card_set_data.at[card_order[curr_card_info['card_num']], card_front.get()]
        l_button.grid_forget()
    else:
        # Flip card to answer side.
        # TODO: allow backing up?
        if DEBUG:
            print("Here's the answer.")
        card_label['text'] = card_set_data.at[card_order[curr_card_info['card_num']], card_back.get()]
        if curr_card_info['card_num'] < len(card_order) - 1:
            r_button['text']="Next"
            l_button['text']="Back"
            l_button['command'] = lambda:advance_flashcard(card_set_data, card_order, curr_card_info, card_label, l_button, r_button, l_button_place_handle,True)
            l_button_place_handle(l_button)
        else:
            r_button['text']="From the top!"
            l_button['text']="Reconfigure."
            # R-button transitions back to init.
            l_button['command'] = lambda:window_transition([window.nametowidget(r_button.winfo_parent())], init_flashcard_set)
            l_button_place_handle(l_button)
        

def begin_flashcards():
    
    doing_flashcards = tk.Frame(window, padx=10, pady=10)
    for col in range(0, 2):
        doing_flashcards.grid_columnconfigure(col, weight=1)
    doing_flashcards.grid(row=1, column=0, sticky=FILL_VOLUME)
    flashcard_l_button = tk.Button(doing_flashcards, text = "...", pady=15, font=MINOR_FONT)
    flashcard_l_button.grid(row=0, column=0, sticky=FILL_VOLUME)
    flashcard_r_button = tk.Button(doing_flashcards, text = "Show", pady=15, font=MINOR_FONT)
    flashcard_r_button.grid(row=0, column=1, sticky=FILL_VOLUME)
    flashcard_set = flashcard_data[[card_front.get(), card_back.get()]]
    if DEBUG:
        print(flashcard_set)
    flashcard_order = list(range(len(flashcard_set)))
    random.shuffle(flashcard_order)
    # Set past the end of the list to force advance_card to start in the right place.
    current_card = {'is_question_side':False, 'card_num':len(flashcard_set)}
    flashcard_r_button['command']= lambda:advance_flashcard(flashcard_set, flashcard_order, current_card, flashcard, flashcard_l_button, flashcard_r_button, lambda card:card.grid(row=0, column=0, sticky=FILL_VOLUME))
    flashcard_r_button.invoke()

def init_flashcard_set():
    flashcard['text'] = "Choose the flashcards'\n front and back."
    flashcard_settings = tk.Frame(window, padx=10, pady=10)
    flashcard_settings.grid(row=1, column=0, sticky=FILL_VOLUME)
    for row in range(0,2):
        flashcard_settings.grid_rowconfigure(row, weight=1)
    for col in range(0, 4):
        flashcard_settings.grid_columnconfigure(col, weight=1)

    card_front_label = tk.Label(flashcard_settings, text="Front: ", font=MINOR_FONT)
    card_front_label.grid(row=0, column=0, sticky=FILL_VOLUME)

    card_front_dropdown = tk.OptionMenu(flashcard_settings, card_front, *data_columns)
    card_front_dropdown.config(font=MINOR_FONT)
    # Yes, the font for the dropdown needs to include the menu, _TKINTER_. What's wrong with you?!
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



