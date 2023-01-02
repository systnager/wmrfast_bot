import json
from tkinter import Tk, ttk
from res.string import strings


def main():
    settings_file = open("settings.json")
    settings = json.load(settings_file)
    settings_file.close()

    root = Tk()
    root.geometry("250x75")
    root.resizable(False, False)
    frame = ttk.Frame(root)
    frame.grid()

    ttk.Button(frame, text=strings["start_watch_youtube"][settings["language"]], width=40).grid(column=0, row=0)
    ttk.Button(frame, text=strings["settings"][settings["language"]], width=40).grid(column=0, row=1)
    ttk.Button(frame, text=strings["exit"][settings["language"]], width=40, command=root.destroy).grid(column=0, row=2)

    root.mainloop()


if __name__ == "__main__":
    main()
