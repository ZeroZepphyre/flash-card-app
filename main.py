from tkinter import *
import pandas
import os
import random, math, functools
# Constantes
BACKGROUND_COLOR = "#B1DDC6"
LANG_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
# Var
timer = None
cur_word_index = None
# Pegando dados do CSV
script_dir = os.path.dirname(__file__)
try:
    file_r_path = "data/words_to_learn.csv"
    absolute_f_path = os.path.join(script_dir, file_r_path)
    file_data = pandas.read_csv(absolute_f_path)
except FileNotFoundError:
    file_r_path = "data/italian_words.csv"
    absolute_f_path = os.path.join(script_dir, file_r_path)
    file_data = pandas.read_csv(absolute_f_path)

# Pegando as Imagens
card_back_path = os.path.join(script_dir, "images/card_back.png")
card_front_path = os.path.join(script_dir, "images/card_front.png")
right_path = os.path.join(script_dir, "images/right.png")
wrong_path = os.path.join(script_dir, "images/wrong.png")

# Palavras em dict
dict_data = pandas.DataFrame(file_data).to_dict('records')
# Funções dos Botões

def change_flashcard(state):
    global cur_word_index
    try:
        if state == "right":
            dict_data.remove(cur_word_index)
            relative_path = "data/words_to_learn.csv"
            absolute_path = os.path.join(script_dir, relative_path)
            pandas.DataFrame(dict_data).to_csv(absolute_path, mode='w')
    except TypeError:
        pass
    try:
        window.after_cancel(timer)
    except ValueError:
        pass

    cur_word_index = random.randint(0, len(dict_data)-1)
    cur_word_italian = dict_data[cur_word_index]["ITALIAN"]
    canvas.itemconfig(canvas_lang, text="Italian", font=LANG_FONT)
    canvas.itemconfig(canvas_img, image=card_front_image)
    canvas.itemconfig(canvas_word, text=cur_word_italian, font=WORD_FONT)

    flip_card(5)

def flip_card(count):
    if math.floor(count) > 0:
        global timer
        timer = window.after(1000, flip_card, count-1)
    if math.floor(count) == 0:
        canvas.itemconfig(canvas_img, image=card_back_image, anchor="nw")
        canvas.itemconfig(canvas_lang, text="English", font=LANG_FONT)
        canvas.itemconfig(canvas_word, text=dict_data[cur_word_index]["ENGLISH"])




# Interface do Usuário
window = Tk()
window.title("Flash Cards: Italian")
window.config(width=1000, height=700, pady=50, padx=50, background=BACKGROUND_COLOR)

wrong_image = PhotoImage(file=wrong_path)
right_image = PhotoImage(file=right_path)
card_back_image = PhotoImage(file=card_back_path)
card_front_image = PhotoImage(file=card_front_path)

wrong_change = functools.partial(change_flashcard, "wrong")
button_wrong = Button(image=wrong_image, highlightthickness=0, borderwidth=0, activebackground=BACKGROUND_COLOR, command=wrong_change)
button_wrong.grid(row=2, column=0)

right_change = functools.partial(change_flashcard, "right")
button_right = Button(image=right_image, highlightthickness=0, borderwidth=0, activebackground=BACKGROUND_COLOR, command=right_change)
button_right.grid(row=2, column=1)


canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
canvas_img = canvas.create_image(0, 0, image=card_front_image, anchor="nw")
canvas_lang = canvas.create_text(400, 150, text="Italian", font=LANG_FONT)
canvas_word = canvas.create_text(400, 236, text="Press Any Button to Start", font=("Ariel", 30, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


window.mainloop()