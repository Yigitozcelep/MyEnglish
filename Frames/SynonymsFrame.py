from tkinter import *
import Style
from DataBase import do_synonyms

class Synonyms:
    def __init__(self, root, row, column):
        self.frame = Frame(root, height=70, width=1300, bg="black", border=5, relief="solid")
        self.frame.grid(row=row, column=column)
        self.frame.grid_propagate(0)
        self.current = "black"

    def change(self, info, word):
        for widget in self.frame.winfo_children():
            widget.grid_remove()


        if info == "brown":
            self.current = "brown"
            self.frame.config(bg=Style.CL_BROWN2)
            if not "|" in word.synonyms: word.synonyms = " | " + word.synonyms
            buttons_data, label_data = word.synonyms.split("|")
            buttons_data, label_data = [x.strip() for x in buttons_data.split(",") if x.strip()], [x.strip() for x in label_data.split(",") if x.strip()]
            index = 0
            for index,word in enumerate(buttons_data, start=0):
                x = Button(self.frame, text=str(word), bg=Style.CL_BROWN2, fg="black", font=("helvetica", 21, "bold"), command= lambda word=word: PopUp(word))
                x.grid(row=0, column=index, pady=10, padx=5)

            for index, word in enumerate(label_data, start=index +1):
                x = Label(self.frame, text=str(word), bg=Style.CL_BROWN2, fg="black", font=("helvetica", 21, "bold"), border=3, relief="solid", padx=2, pady=2)
                x.grid(row=0, column=index, pady=5, padx=5)

        elif info == "black":
            self.current = "black"
            self.frame.config(bg="black")

    def delete_synonyms(self):
        for x in self.frame.winfo_children():
            x.grid_remove()


class PopUp:
    def __init__(self, word):
        self.root = Toplevel(bg=Style.CL_BROWN2)
        data = {key: value for key, value in word.__dict__.items() if value and key != "list_t_f"}.items()
        for index, (key, value) in enumerate(data):
            x = Label(self.root, text=key + f": {value}", font=("helvetica", 20, "bold"), bg=Style.CL_BROWN2, fg="black", border=2, relief="solid")
            x.grid(row=index // 2, column=index % 2, padx=10, pady=10, sticky=W)




