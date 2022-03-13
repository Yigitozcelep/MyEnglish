from tkinter import *
import Style

class FirstScreen:
    def __init__(self, root, row, column):
        self.check_frame = Frame(root, background=Style.CL_BROWN1, width=1300, height=600)
        self.check_frame.grid(row=row, column=column)
        self.check_frame.grid_propagate(0)
        self.widgets = []
        self.frames = []
        for row in range(5):
            x = Frame(self.check_frame, height=120, width=1300, bg=Style.CL_BROWN1, borderwidth=5, relief="solid")
            x.grid(row=row, column=0)
            x.grid_propagate(0)
            self.frames.append(x)

        for row in range(5):
            big = Label(self.frames[row], font=("helvetica", 37, "bold"), text=f"Fnish: ", bg=Style.CL_BROWN1,fg="pink", anchor="center")
            big.grid(row=row, column=0, padx=(10,0))

            small = Label(self.frames[row], font=("helvetica", 29, "bold"), text="falan fistan" * 10, bg=Style.CL_BROWN1, fg="orange", wraplength=1000, height=3, anchor="center")
            small.grid(row=row, column=1)
            self.widgets.append((big, small))


    def fnish(self):
            for l1, l2 in self.widgets:
                l1.config(text="Fnish")
                l2.config(text="Fnish")

    def grid_widgets(self):
        for l1,l2 in self.widgets:
            l1.grid(row=0, column=0)
            l2.grid(row=0, column=1)
    def change_screen(self, word, info):
        for l1,l2 in self.widgets:l1.config(text=""),l2.config(text="")

        for num, name in enumerate(word.major_attributes()):
            writed_name = name if name != "adjective" else "adj"
            l1, l2 = self.widgets[num]
            if info == "first":
                l1.config(text=(writed_name + ": ").capitalize())
                w1,w2 = word.__dict__[name + '_tr1'], word.__dict__[name + '_tr2']
                l2.config(text=f"{w1}{' ~ ' + w2 if w2 else ''}")
            elif info == "second":
                w1, w2 = word.__dict__[name + '_ex1'], word.__dict__[name + '_ex2']
                l1.config(text=word.__dict__[name] + ":")
                l2.config(text=f"{w1}{' ~ ' + w2 if w2 else ''}")








