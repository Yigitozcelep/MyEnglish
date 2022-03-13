from tkinter import *
import random
import Style

class Quiz:
    def __init__(self, current, word_list, frame: Tk):
        self.movable_entries = []
        self.part = 1
        self.words = word_list [current -5: current]
        self.buttons = set()
        self.is_fnish = False
        self.old_quiz_data = []

        for widget in frame.winfo_children()[1].winfo_children():
            widget.grid_forget()

        for num,word in enumerate(self.words):
            frame.winfo_children()[1].configure(bg=Style.CL_BROWN2)
            Label(frame.winfo_children()[1], text=str(word), font=("helvetica", 30, "bold"), bg=Style.CL_BROWN2, fg="black").grid(row=0, column=num, pady=8, padx=10)

        self.frames = frame.winfo_children()[0].winfo_children()
        for frame in self.frames:
            for widgets in frame.winfo_children():
                widgets.grid_forget()

        random.shuffle(self.words)
        self.create_entries()


    def create_entries(self):
        for num,word in enumerate(self.words):
            x = Entry(self.frames[num],font=("helvetica", 25, "bold"), bg=Style.CL_BROWN1, fg="orange", highlightbackground="brown", width=83)
            quiz, answer = self.chose_quiz_ex(word)
            self.old_quiz_data.append((quiz, answer))
            x.insert(0, quiz.replace(answer, " *** ", 1))
            x.word_coor = quiz.find(answer)
            x.answer = answer
            x.quiz = quiz
            x.my_word = word
            x.grid(row=0, column=0, ipady=8, pady=(15,5), padx=6)
            self.movable_entries.append(x)

    def create_for_back(self):
        for num,word in enumerate(self.words):
            x = Entry(self.frames[num],font=("helvetica", 25, "bold"), bg=Style.CL_BROWN1, fg="orange", highlightbackground="brown", width=83)
            quiz, answer = self.old_quiz_data[num]
            x.insert(0, quiz.replace(answer, " *** ", 1))
            x.word_coor = quiz.find(answer)
            x.answer = answer
            x.quiz = quiz
            x.my_word = word
            x.grid(row=0, column=0, ipady=8, pady=(15,5), padx=6)
            self.movable_entries.append(x)



    def chose_quiz_ex(self, word):
        random_word = [x for x in [word.quiz1, word.quiz2, word.quiz3, word.quiz4] if x]
        if random_word:
            result = random.choice(random_word)
        else:
            result = ""
        if not result: return result, ""

        data_result = [x.strip() for x in result.split(" ")]
        for att in word.major_attributes():
            new_att = word.__getattribute__(att)
            for part in data_result:
                if new_att in part:
                    if not part[-1].isalpha(): part = part[:-1]
                    return result, part

        for att in word.major_attributes():
            new_att = word.__getattribute__(att)[:-1]
            for part in data_result:
                if new_att in part:
                    if not part[-1].isalpha(): part = part[:-1]
                    return result, part

        return result, ""


    def set_cursor(self, my_entry):
        my_entry.focus()
        if type(my_entry) == Entry:
            text = my_entry.get()
            result = text[my_entry.word_coor + 1:].find(" ") + my_entry.word_coor + 1
            if self.part == 1:my_entry.icursor(result)
            else:my_entry.icursor("end")
        elif type(my_entry) == Button:
            my_entry.configure(highlightbackground="green")

    def update_word_false(self, word, number):
        word.list_t_f.append(0)
        self.buttons.discard(self.frames[number].winfo_children()[-1])
        self.frames[number].winfo_children()[-1].destroy()


    def show_answer(self):
        for num, entry in enumerate(self.movable_entries):
            entry_text = entry.get()
            if entry.answer in entry_text:
                entry.configure(highlightbackground="green")
                entry.my_word.list_t_f.append(1)
            else:
                entry.configure(highlightbackground="brown")

                my_func = lambda number=num: self.update_word_false(self.words[number], number)
                x = Button(self.frames[num], text="Save as False",border=5, command=my_func , highlightbackground=Style.CL_BROWN1)
                x.grid(row=1, column=0)
                x.my_func = my_func
                x.my_word = self.frames[num].winfo_children()[2].my_word
                self.buttons.add(x)

            entry.delete(0, END)
            entry.insert(0, entry.quiz)

    def fnish(self):
        for x in self.buttons:
            x.my_word.list_t_f.append(1)

        self.is_fnish = True
        for x in self.buttons:
            x.grid_remove()
        for x in self.movable_entries:
            x.grid_remove()



    def clear_button_focus(self):
        for button in self.buttons:
            button.configure(highlightbackground=Style.CL_BROWN1)

    def quiz_keyboard_interactions(self, info, my_entry):
        if info == "Up":
            self.up_key()
        if info == "Down":
            self.down_key()

        if info == "Tab":
            if self.part == 2:
                self.clear_button_focus()

            self.set_cursor(my_entry)

        elif info == "Return":
            if type(self.frames[0].focus_get()) == Button:
                result = self.frames[0].focus_get().tk_focusNext()
                self.frames[0].focus_get().my_func()
                result.focus()
                return

            self.part += 1
            if self.part == 2:
                self.show_answer()
            if self.part == 3:
                self.fnish()
                pass

    def down_key(self):
        result = self.frames[0].focus_get().tk_focusNext()
        if self.part == 2:
            self.clear_button_focus()
        self.set_cursor(result)
    def up_key(self):
        result = self.frames[0].focus_get().tk_focusPrev()
        if self.part == 2:
            self.clear_button_focus()
        self.set_cursor(result)





