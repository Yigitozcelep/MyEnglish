from tkinter import *
import random
import Style
from tkinter.messagebox import showerror
import DataBase as DB
import helper_functions as hf
class SearchButton:
    def __init__(self, root, row, column, font, padx, pady, highlightbackground, main_object):
        self.button = Button(root, text="Search", font=font, highlightbackground=highlightbackground, takefocus=0, command=lambda: PopUp(main_object))
        self.button.grid(row=row, column=column, padx=padx, pady=pady)


class PopUp:
    def __init__(self, main_object):
        self.word_list = main_object.all_words
        self.widgets = []
        self.root = Tk()
        self.root.bind("<Key>", self.key_interactions)
        self.root.configure(bg=Style.CL_BROWN2)
        self.root.geometry("500x500+700+300")
        self.label = Label(self.root, text="Search entry", font=("helvetica", 30, "bold"), bg=Style.CL_BROWN2, fg="black")
        self.label.grid(row=0, column=0, pady=(10,0))
        self.entry = Entry(self.root, font=("helvetica", 30, "bold"), bg="black", fg="orange")
        self.entry.grid(row=1, column=0, padx=70, pady=10)
        if len(self.word_list) < 6:
            showerror("error", "your total world count is lower then < 6 it should be higher then 6")
            self.root.destroy()
            return
        random_word = random.choices(self.word_list, k=5)
        for number,word in enumerate(random_word, start=2):
            x = Button(self.root, text=str(word), font=("helvetica", 30, "bold"), command= lambda word=word: CreateEdit(word))
            x.grid(row=number, column=0, pady=10)
            self.widgets.append(x)

    def key_interactions(self, event):
        if self.root.focus_get() != self.entry: return
        for x in self.widgets:
            x.grid_remove()
        data = []
        text = self.entry.get()
        for word in self.word_list:
             if text in [word.__dict__[x][:len(text)] for x in word.major_attributes()]:
                 data.append(word)

        for number,word in enumerate(data[:5], start=2):
            x = Button(self.root, text=str(word), font=("helvetica", 30, "bold"),
                       command=lambda word=word: CreateEdit(word))
            x.grid(row=number, column=0, pady=10)
            self.widgets.append(x)



class CreateEdit:
    def __init__(self, word):
        self.root = Tk()
        self.root.configure(bg=Style.CL_BROWN2)
        self.widgets = {}
        self.word = word

        data = {key: value for key, value in word.__dict__.items() if key != "id" and key != "list_t_f" and key != "date"}
        row, col = 0, 0
        for key, value in data.items():
            label = Label(self.root, text=key, bg=Style.CL_BROWN2, fg="black", font=("helvetica", 25, "bold"))
            label.grid(row=row, column=col)
            col += 1
            entry = Entry(self.root, font=("helvetica", 25, "bold"), fg="orange")
            entry.grid(row=row, column=col, pady=5, padx=5)
            entry.insert(0, value)
            self.widgets[key] = entry
            col += 1
            if col % 6 == 0:
                col = 0
                row += 1

        self.edit_button = Button(self.root, text="Save", highlightbackground=Style.CL_GREY,
                                  font=("helvetica", 60, "bold"), command=self.click)
        self.edit_button.grid(row=row + 1, column=2, columnspan=2, pady=25, ipadx=60)


    def click(self):
        data = hf.check_validty({key: entry.get() for key, entry in self.widgets.items()}, info="show")
        print(f"data: {data}")
        if data:
            current_word = self.word
            data["id"] = current_word.id
            DB.update_word(data)
            data["date"] = current_word.date
            data["list_t_f"] = current_word.list_t_f
            current_word.__dict__ = data
            showerror("error", "word succesfully added")
            self.root.destroy()
