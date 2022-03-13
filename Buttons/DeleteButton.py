from tkinter import *
from tkinter.messagebox import askyesno, showerror
class DeleteButton:
    def __init__(self, root, row, column, font, padx, pady, highlightbackground, main_object):
        self.button = Button(root, text="Delete", font=font, highlightbackground=highlightbackground, takefocus=0, command=self.delete_word)
        self.button.grid(row=row, column=column, padx=padx, pady=pady)
        self.main_object = main_object

    def delete_word(self):
        answer = askyesno("error", "are you sure you can not back your action")
        if answer:
            showerror("error", "this word will be deleted after the all word finish even if you press the back button")
            self.main_object.will_delete.add(self.main_object.word_list[self.main_object.current])
            self.main_object.next_word("false")

    def disable_button(self):
        self.button.configure(state=DISABLED)

    def enable_button(self):
        self.button.configure(state=NORMAL)
