from tkinter import ALL, Button, Canvas, Checkbutton, Frame, IntVar, Label, Scrollbar
from typing import Any, Callable, List
from models.domain.entity import Stickers
from client.app import App

class ItemListSticker(Frame):
    sticker: Stickers

    def __init__(self, window: Frame, sticker: Stickers):
        super().__init__(window, highlightbackground="gray", highlightthickness=1, pady=5)
        self.columnconfigure(2, weight=1)
        self.sticker = sticker

        self.selected = IntVar()
        Checkbutton(self, onvalue=1, offvalue=0, variable=self.selected).grid(row=0, column=0, rowspan=3)

        Label(self, text="Nome:", padx=5).grid(row=0, column=1, sticky="w")
        Label(self, text=self.sticker.playername, padx=5).grid(row=0, column=2, sticky="w")
        
        Label(self, text="País:", padx=5).grid(row=1, column=1, sticky="w")
        Label(self, text=self.sticker.country, padx=5).grid(row=1, column=2, sticky="w")

        Label(self, text="Raridade:", padx=5).grid(row=2, column=1, sticky="w")
        Label(self, text=str(self.sticker.rarity), padx=5).grid(row=2, column=2, sticky="w")

    def is_selected(self):
        return self.selected.get()


class ListSticker(Frame):
    view_list: List[ItemListSticker]

    def __init__(self, window: Frame):
        super().__init__(window)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = Canvas(self, bg="blue")
        self.canvas.grid(column=0, row=0, sticky="snew")

        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scroll.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox(ALL)))

        self.content = Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0,0), window=self.content, anchor="nw")

        self.content.bind('<Configure>', self._frame_configure)
        self.canvas.bind('<Configure>', self._change_frame_width)

        self.view_list = []

    def get_selected_stickers(self):
        selected = []
        for item in self.view_list:
            if item.is_selected():
                selected.append(item.id)
        return selected

    def update_view(self):
        for v in self.view_list:
            v.pack_forget()
            v.destroy()
        self.view_list.clear()

    def add_sticker(self, sticker: Stickers):
        item = ItemListSticker(self.content, sticker=sticker)
        item.pack(fill="x")
        self.view_list.append(item)

    def _change_frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

    def _frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class TradeView(Frame):
    def __init__(self, window: App):
        super().__init__(window, bg="green")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        Label(self, text="Minhas Figurinhas", pady=15, highlightbackground="gray", highlightthickness=1).grid(row=0, column=0, sticky="we")
        self.my_list = ListSticker(self)
        self.my_list.grid(row=1, column=0, sticky="snew")

        self.other_name_lbl = Label(self, text="Figurinhas de ", pady=15, highlightbackground="gray", highlightthickness=1)
        self.other_name_lbl.grid(row=0, column=1, sticky="we")  

        self.other_list = ListSticker(self)
        self.other_list.grid(row=1, column=1, sticky="snew")

        Button(self, text="Solicitar Troca", command=self._trade, padx=10).grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    
    def add_my_stickers(self, stickers: List[Stickers]):
        for v in stickers:
            self.my_list.add_sticker(v)

    def add_other_stickers(self, stickers: List[Stickers]):
        for v in stickers:
            self.other_list.add_sticker(v)

    def clear(self):
        self.my_list.clear()
        self.other_list.clear()
        self.other_name_lbl.config(text="Figurinhas de ")

    def _trade(self):
        my_stickers = self.my_list.get_selected_stickers()
        other_stickers = self.other_list.get_selected_stickers()

        sticker = Stickers(playername="Neymar", country="Brasil", rarity=1)
        self.my_list.add_sticker(sticker=sticker)

        