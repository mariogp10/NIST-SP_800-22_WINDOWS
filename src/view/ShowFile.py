import os
import tkinter as tk
from tkinter import scrolledtext

class ShowFile():
    def __init__(self, mainwin, title, dir_location):
        self.mainwin = mainwin
        self.SFWin = tk.Toplevel(mainwin)
        self.SFWin.title(title)
        self.text_area = scrolledtext.ScrolledText(self.SFWin)
        self.text_area.pack(expand=False, fill='both')
        if os.path.exists(dir_location):
            with open(dir_location, "r") as file:
                content = file.read()
        else:
            content = "Este archivo esta vacio."
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, content)
        self.text_area.configure(state=tk.DISABLED)