import json
import tkinter
from tkinter import Tk, ttk
from res.string import strings

settings_file = open("settings.json")
settings = json.load(settings_file)
settings_file.close()


def main():
    global settings
    root = Tk()
    root.geometry("250x75")
    root.resizable(False, False)

    ttk.Button(root, text=strings["start_watch_youtube"][settings["language"]],
               width=40, command=start_watch_youtube()).grid(column=0, row=0)
    ttk.Button(root, text=strings["settings"][settings["language"]],
               width=40, command=open_settings).grid(column=0, row=1)
    ttk.Button(root, text=strings["exit"][settings["language"]],
               width=40, command=root.destroy).grid(column=0, row=2)

    root.mainloop()


def start_watch_youtube():
    pass


def log_in_on_wmrfast():
    pass


def open_settings():
    global settings
    setting_window = tkinter.Toplevel()
    setting_window.resizable(False, False)
    setting_window.title(strings["settings"][settings["language"]])
    setting_window.config(width=250, height=250)

    list_items = tkinter.Variable(value=settings["support_languages"])
    listbox = tkinter.Listbox(setting_window, width=40, height=3, listvariable=list_items)
    listbox.grid(column=0, row=0)
    ttk.Button(setting_window, text=strings["save"][settings["language"]],
               width=40).grid(column=0, row=1)
    ttk.Button(setting_window, text=strings["exit"][settings["language"]],
               width=40, command=setting_window.destroy).grid(column=0, row=2)


def save_settings():
    global settings
    global settings_file
    settings_file = open("settings.json")
    settings_file.write(json.dumps(settings))
    settings_file.close()


if __name__ == "__main__":
    main()
