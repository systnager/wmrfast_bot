import tkinter
from tkinter import Tk

from wmrfast import WMRFast
from settings import Settings
from res.string import strings


class MainWindow:
    def __init__(self):
        self.settings = Settings()
        self.wmrfast = WMRFast()

        self.root = Tk()
        self.root.geometry("250x225")
        self.root.resizable(False, False)

        self.start_watch_youtube = tkinter.Button(self.root, text=strings["start_watch_youtube"][self.settings.
                                                  get_settings()["language"]], width=40, height=2,
                                                  command=self.wmrfast.start_watch_youtube)

        self.start_watch_youtube_forever = tkinter.Button(self.root, text=strings["start_watch_youtube_forever"]
                                                          [self.settings.get_settings()["language"]],
                                                          width=40, height=2, command=self._start_watch_youtube_forever)

        self.exit = tkinter.Button(self.root, text=strings["exit"][self.settings
                                   .get_settings()["language"]], width=40, height=2, command=self.destroy_window)

        self.open_settings = tkinter.Button(self.root, text=strings["settings"][self.settings.get_settings()[
            "language"]], width=40, height=2, command=self.settings.open_edit_settings)

        self.start_watch_youtube_forever.pack(padx=10, pady=5)
        self.start_watch_youtube.pack(padx=10, pady=5)
        self.open_settings.pack(padx=10, pady=5)
        self.exit.pack(padx=10, pady=5)

    def open_window(self):
        self.root.mainloop()

    def destroy_window(self):
        self.root.destroy()

    def _start_watch_youtube_forever(self):
        while True:
            self.wmrfast.start_watch_youtube()
