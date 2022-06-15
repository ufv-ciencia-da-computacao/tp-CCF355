from tkinter import *

class HomepageFrame(Frame):
    def __init__(self, window: Tk):
        super().__init__(window)
        self.grid(row=0, column=0, sticky="nsew")
        self.label = Label(self, text="Hello Homepage")
        self.label.pack()
