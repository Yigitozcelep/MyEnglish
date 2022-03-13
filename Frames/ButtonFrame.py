import Buttons.ShownLabel as SL
import Buttons.BackButton as BB
import Buttons.EditButton as EB
import Buttons.TrainButton as TB
import Buttons.DeleteButton as DB
import Buttons.AddButton as AB
import Buttons.SearchButton as SB
from tkinter import *
import Style

class ButtonFrame:
    def __init__(self, root, row, column, main_object):
        # TODO SEARCH BUTTONU EKLE
        self.button_frame = Frame(root, bg=Style.CL_BROWN2,borderwidth=5, relief="solid", height=120, width=1300)
        self.button_frame.grid(row=row, column=column)
        self.button_frame.grid_propagate(0)
        self.main_object = main_object

        self.back_button = BB.BackButton(self.button_frame, **Style.B_STYLES_1,row=0, column=0, main_object=self.main_object)
        self.edit_button = EB.EditButton(self.button_frame, **Style.B_STYLES, row=0, column=1, main_object=self.main_object)
        self.train_button = TB.TrainButton(self.button_frame, **Style.B_STYLES, row=0, column=2, main_object=self.main_object)
        self.delete_button = DB.DeleteButton(self.button_frame, **Style.B_STYLES, row=0, column=3, main_object=self.main_object)
        self.add_button = AB.AddButton(self.button_frame, **Style.B_STYLES, row=0, column=4)
        self.search_button = SB.SearchButton(self.button_frame, **Style.B_STYLES, row=0, column=5, main_object=self.main_object)
        self.shown_label = SL.ShownLabel(self.button_frame, **Style.L_STYLES, row=0, column=6)

    def disable_unnecessery_buttons(self):
        self.back_button.disable_button()
        self.delete_button.disable_button()
        self.edit_button.disable_button()

    def enable_buttons(self):
        self.back_button.enable_button()
        self.delete_button.enable_button()
        self.edit_button.enable_button()