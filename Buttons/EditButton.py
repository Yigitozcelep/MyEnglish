from tkinter import *
import helper_functions as hf
import Style
import DataBase as DB
from tkinter.messagebox import showerror
class EditButton:
    def __init__(self, root, row, column, font, padx, pady, highlightbackground, main_object):
        self.button = Button(root, text="Edit", font=font, highlightbackground=highlightbackground, takefocus=0, command=self.create_popup)
        self.button.grid(row=row, column=column, padx=padx, pady=pady)
        self.main_object = main_object
        self.widgets = {}

    def disable_button(self):
        self.button.configure(state=DISABLED)

    def enable_button(self):
        self.button.configure(state=DISABLED)

    def create_popup(self):
        if self.main_object.part == "quiz":
            showerror("error", "you can not edit in quiz part")
            return

        top_level = Toplevel(padx=20, pady=20, bg=Style.CL_BROWN2)
        top_level.geometry("1450x700+200+150")
        data = self.main_object.word_list[self.main_object.current].__dict__
        data = {key: value for key, value in data.items() if key != "id" and key != "list_t_f" and key != "date"}
        row, col = 0, 0
        for key, value in data.items():
            label = Label(top_level, text=key, bg=Style.CL_BROWN2, fg="black", font=("helvetica", 25, "bold"))
            label.grid(row=row, column=col)
            col += 1
            entry = Entry(top_level, font=("helvetica", 25, "bold"), fg="orange")
            entry.grid(row=row, column=col, pady=5, padx=5)
            entry.insert(0, value)
            self.widgets[key] = entry
            col += 1
            if col % 6 == 0:
                col = 0
                row += 1

        self.edit_button = Button(top_level, text="Save", highlightbackground=Style.CL_GREY, font=("helvetica", 60, "bold"), command=self.click)
        self.edit_button.grid(row=row + 1, column=2, columnspan=2, pady=25, ipadx=60)


    def click(self):
        data = hf.check_validty({key: entry.get() for key, entry in self.widgets.items()}, info="show")
        if data:
            current_word = self.main_object.word_list[self.main_object.current]
            data["id"] = current_word.id
            print(data)
            DB.update_word(data)
            data["date"] = current_word.date
            data["list_t_f"] = current_word.list_t_f
            current_word.__dict__ = data
            showerror("error", "it is successfully saved press up and down commands to see changes")


