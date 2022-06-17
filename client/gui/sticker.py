from tkinter import *

class StickerFrame(Frame):
    def __init__(self, window: Tk):
        super().__init__(window, width=180, height=250, bg="green")
        self.pack_propagate(False)
        self.window = window
        