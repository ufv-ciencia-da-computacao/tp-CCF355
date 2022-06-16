from tkinter import *
from gui.sticker import StickerFrame

class HomepageFrame(Frame):
    def __init__(self, window: Tk):
        super().__init__(window)
        self.grid(row=0, column=0, sticky="nsew")

        StickerFrame(self).pack(side="left", padx=10)
        StickerFrame(self).pack(side="left", padx=10)
        StickerFrame(self).pack(side="left", padx=10)
        StickerFrame(self).pack(side="left", padx=10)
        StickerFrame(self).pack(side="left", padx=10)
        StickerFrame(self).pack(side="left", padx=10)
