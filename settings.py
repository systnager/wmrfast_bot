import json
import tkinter
from tkinter import ttk

from res.string import strings


class Settings:
    def __init__(self):
        settings_file = open("settings.json")
        self.settings = json.load(settings_file)
        settings_file.close()

    def get_settings(self):
        return self.settings

    def save_settings(self):
        settings_file = open("settings.json")
        settings_file.write(json.dumps(self.settings))
        settings_file.close()

    def open_edit_settings(self):
        setting_window = tkinter.Toplevel()
        setting_window.resizable(False, False)
        setting_window.title(strings["settings"][self.settings["language"]])
        setting_window.config(width=250, height=250)

        list_items = tkinter.Variable(value=self.settings["support_languages"])

        listbox = tkinter.Listbox(setting_window, width=40, height=3, listvariable=list_items)
        ttk.Button(setting_window, text=strings["save"][self.settings["language"]],
                   width=40).grid(column=0, row=1)
        ttk.Button(setting_window, text=strings["exit"][self.settings["language"]],
                   width=40, command=setting_window.destroy).grid(column=0, row=2)

        listbox.grid(column=0, row=0)
        listbox.selection_set(0)
