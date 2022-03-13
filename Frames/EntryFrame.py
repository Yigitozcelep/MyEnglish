from tkinter import *
import Style
from DataBase import do_synonyms
class EntryFrame:
    def __init__(self, root, row, column):
        self.check_frame = Frame(root, background=Style.CL_BROWN2, width=1300, height=170, borderwidth=5, relief="solid")
        self.check_frame.grid(row=row, column=column)
        self.check_frame.grid_propagate(0)
        self.widgets = []

        self.noun_label = Label(self.check_frame, text="Noun:", font=("helvetica", 25 , "bold"), bg=Style.CL_BROWN2, fg="black")
        self.noun_label.grid(row=0, column=0, padx=(30,0))
        self.noun_entry = Entry(self.check_frame, font=("helvetica", 25, "bold"), takefocus=1, disabledbackground="brown", fg="orange")
        self.noun_entry.grid(row=0, column=1, columnspan=5, pady=25)

        self.adjective_label = Label(self.check_frame, text="Adjective:", font=("helvetica", 25, "bold"), bg=Style.CL_BROWN2,fg="black")
        self.adjective_label.grid(row=0, column=6, padx=(10,0))
        self.adjective_entry = Entry(self.check_frame, font=("helvetica", 25, "bold"), takefocus=1,  disabledbackground="brown", fg="orange")
        self.adjective_entry.grid(row=0, column=7, columnspan=5)

        self.verb_label = Label(self.check_frame, text="Verb: ", font=("helvetica", 25, "bold"), bg=Style.CL_BROWN2, fg="black")
        self.verb_label.grid(row=0, column=12, padx=(10,0))
        self.verb_entry = Entry(self.check_frame, font=("helvetica", 25, "bold"), takefocus=1,  disabledbackground="brown", fg="orange")
        self.verb_entry.grid(row=0, column=13, columnspan=5)

        self.adverb_label = Label(self.check_frame, text="Adverb:", font=("helvetica", 25, "bold"), bg=Style.CL_BROWN2,fg="black")
        self.adverb_label.grid(row=1, column=2, sticky=E)
        self.adverb_entry = Entry(self.check_frame, font=("helvetica", 25, "bold"), takefocus=1, disabledbackground="brown", fg="orange")
        self.adverb_entry.grid(row=1, column=3, columnspan=5, sticky=W)

        self.phrase_label = Label(self.check_frame, text="Phrase:", font=("helvetica", 25, "bold"), bg=Style.CL_BROWN2, fg="black", )
        self.phrase_label.grid(row=1, column=9, sticky=E)
        self.phrase_entry = Entry(self.check_frame, font=("helvetica", 25, "bold"), takefocus=1,  disabledbackground="brown", fg="orange")
        self.phrase_entry.grid(row=1, column=10, columnspan=5, sticky=W)

        self.widgets.append(("noun", self.noun_entry))
        self.widgets.append(("adjective", self.adjective_entry))
        self.widgets.append(("verb", self.verb_entry))
        self.widgets.append(("adverb", self.adverb_entry))
        self.widgets.append(("phrase", self.phrase_entry))


    def check_word(self, word):
        for part,entry in self.widgets:
            entry.configure(state=DISABLED)
            entry.configure(takefocus=0)

        for part, entry in self.widgets:
            if word.__getattribute__(part):
                entry.configure(state=NORMAL)
                entry.configure(takefocus=1)

    def clear_entries(self):
        for part, entry in self.widgets:
            entry.delete(0, END)
            entry.configure(state=DISABLED, highlightbackground="black")
            entry.configure(takefocus=0)
            self.check_frame.focus()

    def check_word_t_f(self, word):
        for part, entry in self.widgets:
            if not entry.cget("state") == "normal":continue
            data = {x.strip() for x in entry.get().split(",") if x.strip()}
            if [x for x in data if x in word.__getattribute__(part)]:
                entry.configure(highlightbackground="green")
            else:
                entry.configure(highlightbackground="red")
