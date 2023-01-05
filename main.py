import json
import tkinter
from tkinter import Tk, ttk

from settings import Settings
from res.string import strings


def main():
    root = Tk()
    root.geometry("250x75")
    root.resizable(False, False)

    settings = Settings()

    ttk.Button(root, text=strings["start_watch_youtube"][settings.get_settings()["language"]],
               width=40, command=start_watch_youtube).grid(column=0, row=0)
    ttk.Button(root, text=strings["settings"][settings.get_settings()["language"]],
               width=40, command=lambda: settings.open_edit_settings()).grid(column=0, row=1)
    ttk.Button(root, text=strings["exit"][settings.get_settings()["language"]],
               width=40, command=root.destroy).grid(column=0, row=2)

    root.mainloop()


def start_watch_youtube():
    pass


def log_in_on_wmrfast():
    pass


if __name__ == "__main__":
    main()
