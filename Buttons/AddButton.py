import datetime
from AutoWord import auto_word as aw
import time
from tkinter import *
import Style
import DataBase as DB
import helper_functions as hf
class AddButton:
    def __init__(self, root, row, column, font, padx, pady, highlightbackground):
        self.button = Button(root, text="Add", font=font, highlightbackground=highlightbackground, command=AddPage, takefocus=0)
        self.button.grid(row=row, column=column, padx=padx, pady=pady)

class AddPage:
    def __init__(self):
        self.widgets = {}
        self.add_root = Tk()
        self.add_root.configure(bg=Style.CL_BROWN2, padx=20)
        self.add_root.bind("<Return>", lambda x: self.auto_click(x))
        self.add_root.geometry("1600x600+100+200")
        checker = 0
        for row in range(8):
            for column in range(0,8,2):
                x = Label(self.add_root, text=Style.ALL_ATT[checker], **Style.AP_L_STYLES)
                x.grid(row=row, column=column, pady=10)
                checker += 1
                y = Entry(self.add_root, font=("helvetica", 20, "bold"), fg="orange")
                y.grid(row=row,column= column+1, pady=2)
                self.widgets[Style.ALL_ATT[checker -1]] = y

        self.widgets["shown"].insert(0, "0")
        self.widgets["frequency"].insert(0, "0-1-7-14-30-90-360")

        self.loading_label = Label(self.add_root, text="Loading...", font=("helvetica", 60, "bold"), fg="black", bg=Style.CL_BROWN2)
        self.loading_label.grid(row=9, column=2, columnspan=2)
        self.loading_label.grid_forget()

        x = Label(self.add_root, text="Auto words", **Style.AP_L_STYLES)
        x.grid(row=8, column=0, sticky=E)
        y = Entry(self.add_root, font=("helvetica", 20, "bold"), width=118, fg="orange")
        y.grid(row=8, column=1, columnspan=7, sticky=W, pady=20)
        self.widgets["auto_words"] = y
        save_button = Button(self.add_root, text="save", **Style.B_STYLES, command=self.click)
        save_button.grid(row=9, column=2, columnspan=3, sticky=E)

    def click(self):
        data = hf.check_validty({name: entry.get() for name, entry in self.widgets.items()}, "show")
        if not data:
            return
        self.loading_label.grid(row=9, column=2, columnspan=2)
        self.loading_label.wait_visibility()
        for key, entry in self.widgets.items():
            if key == "frequency" or key == "shown" or key == "auto_words": continue
            entry.delete(0, END)
        if "auto_words" in data and not data["auto_words"]:
            del data["auto_words"]
            data["date"] = str(datetime.date.today())
            DB.save_word(data)
        elif "auto_words" in data and data["auto_words"]:
            aw.main_auto_word(data["auto_words"])

        self.loading_label.grid_forget()


    def auto_click(self, event):
        self.click()
