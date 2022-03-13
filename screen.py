import Frames.QuizFrame as QF
import datetime
import Frames.EntryFrame as EF
import Frames.FirstScreen as FS
from tkinter import *
import Frames.ButtonFrame as BF
import DataBase as DB
import Frames.SynonymsFrame as SF


class Interface:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1300x960+250+65")
        self.root.title("yigit ozcelep")

        self.root.bind("<Key>", self.key_interactions)
        self.current = 0
        self.word_list = DB.Word.today_words
        self.current_screen = "first"
        self.part = "1"
        self.state = True
        self.all_words = DB.Word.all_words
        self.in_train = False
        self.will_delete = set()
        self.first_screen = FS.FirstScreen(self.root, 0, 0)
        self.synonyms_frame = SF.Synonyms(self.root, 1, 0)
        self.entry_frame = EF.EntryFrame(self.root, 2, 0)
        self.button_frame = BF.ButtonFrame(self.root, 3,0, self)
        self.shown_label = self.button_frame.shown_label

        if not self.word_list:
            self.fnish()
        else:
            self.change_screen(self.word_list[self.current], self.current_screen)
            self.entry_frame.clear_entries()
            self.entry_frame.check_word(self.word_list[self.current])
            DB.change_all_synonyms()
        self.root.mainloop()

    def fnish_quiz(self):
        self.part = "1"
        self.current_screen = "first"
        self.check_next()
        self.first_screen.grid_widgets()
        self.current_screen = "first" if self.part == "1" else "second"
        self.entry_frame.clear_entries()
        self.entry_frame.check_word(self.word_list[self.current])
        self.change_screen(self.word_list[self.current], self.current_screen)

    def key_interactions(self, event):
        if not self.state: return
        if self.part == "quiz":
            self.quiz_frame.quiz_keyboard_interactions(event.keysym, self.root.focus_get().tk_focusNext())
            if self.quiz_frame.part == 3:
               self.fnish_quiz()
            return "break"

        elif event.keysym == "Return":
            self.entry_frame.check_word_t_f(self.word_list[self.current])

        elif event.keysym == "1":
            self.next_word("false")
        elif event.keysym == "2":
            self.next_word("true")
        elif event.keysym == "Up" or event.keysym == "Down":
            self.other_current_screen()
            self.change_screen(self.word_list[self.current], self.current_screen)


    def next_word(self, info):
        self.update_word(info)
        self.current += 1
        if self.part == "1" and self.current % 5 == 0:
            self.entry_frame.clear_entries()
            self.quiz_frame = QF.Quiz(current=self.current, word_list=self.word_list, frame=self.root)
            self.part = "quiz"
            return

        if not self.check_next():return
        self.current_screen = "first" if self.part == "1" else "second"
        self.entry_frame.clear_entries()
        self.entry_frame.check_word(self.word_list[self.current])
        self.change_screen(self.word_list[self.current], self.current_screen)



    def change_screen(self, word, info):

        self.first_screen.change_screen(word, info)
        self.shown_label.change_label(word=word, current_screen=self.current_screen)


        if self.current_screen == "first":
            self.synonyms_frame.change("black",self.word_list[self.current])

        elif self.current_screen == "second":
            self.synonyms_frame.change("brown",self.word_list[self.current])



    def other_current_screen(self):
        if self.current_screen == "first": self.current_screen = "second"
        elif self.current_screen == "second": self.current_screen = "first"

    def check_next(self):
        if self.current == len(self.word_list):
            if self.part == "1":
                self.current = 0
                self.part = "2"
                return True

            elif self.part == "2":
                self.current = 0
                self.fnish()
                return False
        return True

    def do_update_delete_things(self):
        for word in self.word_list:
            if 0 in word.list_t_f:
                DB.update_word({"shown": 0, "date": str(datetime.date.today()), "id": word.id})
            else:
                word.shown += 1
                DB.update_word({"shown": word.shown, "id": word.id})
        for word in self.will_delete:
            DB.delete_word(word.id)

    def restart_app(self):
        self.current = 0
        self.part = "1"
        self.current_screen = "first"
        self.will_delete = set()
        self.change_screen(self.word_list[self.current], self.current_screen)

    def fnish(self):
        if self.in_train:
            self.first_screen.fnish()
            self.button_frame.disable_unnecessery_buttons()
            self.synonyms_frame.delete_synonyms()
            self.state = False
            return

        self.do_update_delete_things()
        DB.Word.all_words = []
        DB.Word.today_words = []
        DB.collect_words()
        self.word_list = DB.Word.today_words

        if self.word_list:
            self.restart_app()
            return

        self.button_frame.disable_unnecessery_buttons()
        self.synonyms_frame.delete_synonyms()
        self.first_screen.fnish()
        self.state = False

    def update_word(self, info):
        if info == "true":
            self.word_list[self.current].list_t_f.append(1)

        elif info == "false":
            self.word_list[self.current].list_t_f.append(0)



Interface()
