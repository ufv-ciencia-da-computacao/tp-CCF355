from tkinter import ALL, Button, Canvas, Checkbutton, Frame, IntVar, Label, Scrollbar
from typing import List
from models.domain.entity import Stickers
from app import App

class ItemListSticker(Frame):
    def __init__(self, window: Frame, name: str, country: str, rarity: int, index: int):
        super().__init__(window, highlightbackground="gray", highlightthickness=1, pady=5)
        self.columnconfigure(2, weight=1)
        
        var = IntVar()
        Checkbutton(self, onvalue=1, offvalue=0, variable=var, command=lambda : print("olá", index, var.get())).grid(row=0, column=0, rowspan=3)

        Label(self, text="Nome:", padx=5).grid(row=0, column=1, sticky="w")
        Label(self, text=name, padx=5).grid(row=0, column=2, sticky="w")
        
        Label(self, text="País:", padx=5).grid(row=1, column=1, sticky="w")
        Label(self, text=country, padx=5).grid(row=1, column=2, sticky="w")

        Label(self, text="Raridade:", padx=5).grid(row=2, column=1, sticky="w")
        Label(self, text=str(rarity), padx=5).grid(row=2, column=2, sticky="w")


class ListSticker(Frame):
    def __init__(self, window: Frame, stickers: List[Stickers], *args, **kwargs):
        super().__init__(window, *args, **kwargs)
        self.stickers = stickers
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = Canvas(self)
        self.canvas.grid(column=0, row=0, sticky="snew")

        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scroll.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox(ALL)))

        self.content = Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0,0), window=self.content, anchor="nw")

        ItemListSticker(self.content, "Neymar", "Brasil", 1, 0).pack(fill="x")
        ItemListSticker(self.content, "Neymar", "Brasil", 1, 1).pack(fill="x")
        ItemListSticker(self.content, "Neymar", "Brasil", 1, 2).pack(fill="x")
        ItemListSticker(self.content, "Neymar", "Brasil", 1, 3).pack(fill="x")
        ItemListSticker(self.content, "Neymar", "Brasil", 1, 3).pack(fill="x")
        ItemListSticker(self.content, "Neymar", "Brasil", 1, 3).pack(fill="x")
        ItemListSticker(self.content, "Neymar", "Brasil", 1, 3).pack(fill="x")
        ItemListSticker(self.content, "Neymar", "Brasil", 1, 3).pack(fill="x")
        ItemListSticker(self.content, "Neymar", "Brasil", 1, 3).pack(fill="x")

        self.content.bind('<Configure>', self._frame_configure)
        self.canvas.bind('<Configure>', self._change_frame_width)

    def _change_frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

    def _frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class ExchangeView(Frame):
    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        Label(self, text="Suas Figurinhas", pady=15, highlightbackground="gray", highlightthickness=1).grid(row=0, column=0, sticky="we")
        ListSticker(self, "user1", None).grid(row=1, column=0, sticky="snew")

        Label(self, text="Figurinhas do outro usuário", pady=15, highlightbackground="gray", highlightthickness=1).grid(row=0, column=1, sticky="we")        
        ListSticker(self, "user2", None).grid(row=1, column=1, sticky="snew")

        Button(self, text="Solicitar Troca", padx=10).grid(row=2, column=0, columnspan=2, padx=10, pady=5)


        