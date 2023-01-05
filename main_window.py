from tkinter import Tk, ttk
from settings import Settings
from res.string import strings


class MainWindow:
    def __init__(self):
        self.settings = Settings()

        self.root = Tk()
        self.root.geometry("250x75")
        self.root.resizable(False, False)

        ttk.Button(self.root, text=strings["start_watch_youtube"][self.settings.get_settings()["language"]],
                   width=40).grid(column=0, row=0)
        ttk.Button(self.root, text=strings["settings"][self.settings.get_settings()["language"]],
                   width=40, command=self.settings.open_edit_settings).grid(column=0, row=1)
        ttk.Button(self.root, text=strings["exit"][self.settings.get_settings()["language"]],
                   width=40, command=self.destroy_window).grid(column=0, row=2)

    def open_window(self):
        self.root.mainloop()

    def destroy_window(self):
        self.root.destroy()
