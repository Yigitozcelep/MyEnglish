from tkinter import *
import Frames.QuizFrame as QF
from tkinter.messagebox import showerror

class BackButton:
    def __init__(self, root, row, column, font, padx, pady, highlightbackground, main_object):
        self.button = Button(root, text="Back", font=font, highlightbackground=highlightbackground, takefocus=0, command=self.click)
        self.button.grid(row=row, column=column, padx=padx, pady=pady)
        self.main_object = main_object

    def disable_button(self):
        self.button.configure(state=DISABLED)

    def enable_button(self):
        self.button.configure(state=NORMAL)


    def back_quit_quiz(self):
        self.main_object.quiz_frame.fnish()
        number = self.main_object.current
        print("quiz exit kısmı")
        for x in range(number-5, number):
            word = self.main_object.word_list[x]
            word.list_t_f = word.list_t_f[:1]

        word = self.main_object.word_list[self.main_object.current - 1]
        word.list_t_f = word.list_t_f[:-1]
        self.main_object.current += -1
        self.main_object.fnish_quiz()

    def back_to_quiz(self):
        number = self.main_object.current
        for x in range(number-5,number):
            word = self.main_object.word_list[x]
            word.list_t_f = word.list_t_f[:-1]

        self.main_object.entry_frame.clear_entries()
        self.main_object.quiz_frame = QF.Quiz(current=self.main_object.current, word_list=self.main_object.word_list, frame=self.main_object.root)
        self.main_object.part = "quiz"

    def back_start_quiz(self):
        self.main_object.quiz_frame.fnish()

        number = self.main_object.current
        for x in range(number - 5, number):
            word = self.main_object.word_list[x]
            word.list_t_f = word.list_t_f[:-1]

        self.main_object.quiz_frame.part = 1
        self.main_object.quiz_frame.is_fnish = False
        self.main_object.quiz_frame.movable_entries = []
        self.main_object.quiz_frame.buttons = set()
        self.main_object.quiz_frame.create_for_back()

    def back_normal(self):
        word = self.main_object.word_list[self.main_object.current - 1]
        word.list_t_f = word.list_t_f[:-1]
        self.main_object.current += -1
        current_screen = "first" if self.main_object.part == "1" else "second"
        self.main_object.change_screen(self.main_object.word_list[self.main_object.current], current_screen)

    def click(self):
        if self.main_object.current == 0:
            showerror("error", "you can not back your action because part is finished")
            return
        if self.main_object.current % 5 == 0 and self.main_object.part == "1":
            self.back_to_quiz()
        elif self.main_object.current % 5 == 0 and self.main_object.part == "quiz":
            if self.main_object.quiz_frame.part == 1:
                self.back_quit_quiz()
            else:
                self.back_start_quiz()

        else:self.back_normal()


