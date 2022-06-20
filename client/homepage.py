from tkinter import *
from app import App

class StickerFrame(Frame):
    def __init__(self, window: Frame):
        super().__init__(window, width=180, height=250, bg="green")
        self.pack_propagate(False)
        self.window = window

class HomepageView(Frame):
    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        content = Frame(self)
        self.canvas = Canvas(content)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        content.grid(row=0, column=0, sticky="we")

        scroll = Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        scroll.grid(row=1, column=0, sticky="we")

        self.canvas.configure(xscrollcommand=scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox(ALL)))

        f = Frame(self.canvas)
        self.canvas.create_window((0,0), window=f, anchor="nw")

        StickerFrame(f).pack(side="left", padx=10)
        StickerFrame(f).pack(side="left", padx=10)
        StickerFrame(f).pack(side="left", padx=10)
        StickerFrame(f).pack(side="left", padx=10)
        StickerFrame(f).pack(side="left", padx=10)
        StickerFrame(f).pack(side="left", padx=10)
