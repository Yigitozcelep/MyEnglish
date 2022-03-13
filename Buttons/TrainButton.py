from tkinter import *
import random
from tkinter.messagebox import showerror
from tkinter.simpledialog import askstring

class TrainButton:
    def __init__(self, root, row, column, font, padx, pady, highlightbackground, main_object):
        self.button = Button(root, text="Train", font=font, highlightbackground=highlightbackground, takefocus=0, command=self.do_train)
        self.button.grid(row=row, column=column, padx=padx, pady=pady)
        self.main_object = main_object

    def do_train(self):
        if self.main_object.part == "quiz":
            showerror("error", "you can not start train mode in quiz")
            return

        count = askstring("question", f"how many word.  max:{len(self.main_object.all_words)}")
        if not count.isnumeric():
            showerror("error", "invalid input. input should be integer")
            return
        if 1 < int(count) > len(self.main_object.all_words):
            showerror("error", "invalid input. input can not be higher then max number or lower then 2")
            return
        count = int(count)
        words = random.choices(self.main_object.all_words, k=count)

        self.main_object.in_train = True
        self.main_object.state = True
        self.main_object.current = 0
        self.main_object.part = "1"
        self.main_object.current_screen = "first"
        self.main_object.word_list = words
        self.main_object.change_screen(words[0], "first")
