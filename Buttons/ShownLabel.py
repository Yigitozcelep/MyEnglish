from tkinter import *

class ShownLabel:
    def __init__(self, root, row, column, font, padx, pady, bg, fg):
        self.row = row
        self.column = column
        self.label = Label(root, text="0", font=font, bg=bg, fg=fg)
        self.label.grid(row=row, column=column, padx=padx, pady=pady)

    def change_label(self, word, current_screen):
        if current_screen == "first":
            self.label.grid_forget()
        elif current_screen == "second":
            self.label.grid(row=self.row, column=self.column)
            self.label.configure(text=word.shown)
