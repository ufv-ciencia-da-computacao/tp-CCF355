from tkinter import (
    ALL,
    END,
    Button,
    Canvas,
    Checkbutton,
    Entry,
    Frame,
    IntVar,
    Label,
    Scrollbar,
)
from typing import List
from client.app import App
import requests
import json


class ItemListSticker(Frame):
    def __init__(self, window: Frame, sticker: dict):
        super().__init__(
            window, highlightbackground="gray", highlightthickness=1, pady=5
        )
        self.columnconfigure(2, weight=1)
        self.sticker = sticker

        self.selected = IntVar()
        Checkbutton(self, onvalue=1, offvalue=0, variable=self.selected).grid(
            row=0, column=0, rowspan=3
        )

        Label(self, text="Nome:", padx=5).grid(row=0, column=1, sticky="w")
        Label(self, text=self.sticker["playername"], padx=5).grid(
            row=0, column=2, sticky="w"
        )

        Label(self, text="País:", padx=5).grid(row=1, column=1, sticky="w")
        Label(self, text=self.sticker["country"], padx=5).grid(
            row=1, column=2, sticky="w"
        )

        Label(self, text="Raridade:", padx=5).grid(row=2, column=1, sticky="w")
        Label(self, text=str(self.sticker["rarity"]), padx=5).grid(
            row=2, column=2, sticky="w"
        )

    def is_selected(self):
        return self.selected.get()


class ListSticker(Frame):
    def __init__(self, window: Frame):
        super().__init__(window)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = Canvas(self)
        self.canvas.grid(column=0, row=0, sticky="snew")

        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scroll.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.config(scrollregion=self.canvas.bbox(ALL)),
        )

        self.content = Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )

        self.content.bind("<Configure>", self._frame_configure)
        self.canvas.bind("<Configure>", self._change_frame_width)

        self.view_list = []

    def get_selected_stickers(self):
        selected = []
        for item in self.view_list:
            if item.is_selected():
                selected.append(item.sticker["id"])
        return selected

    def update_view(self, *args, **kwargs):
        for v in self.view_list:
            v.pack_forget()
            v.destroy()
        self.view_list.clear()

    def add_stickers(self, stickers: List):
        for s in stickers:
            item = ItemListSticker(self.content, sticker=s)
            item.pack(fill="x")
            self.view_list.append(item)

    def clear(self):
        for v in self.view_list:
            v.pack_forget()
        self.view_list.clear()

    def _change_frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def _frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class TradeView(Frame):
    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        my_name = Frame(
            self, pady=15, padx=5, highlightbackground="gray", highlightthickness=1
        )
        my_name.columnconfigure(0, weight=1)
        my_name.rowconfigure(0, weight=1)
        Label(my_name, text="Minhas Figurinhas").grid(row=0, column=0)
        my_name.grid(row=0, column=0, sticky="snew")

        self.my_list = ListSticker(self)
        self.my_list.grid(row=1, column=0, sticky="snew")

        search = Frame(
            self, pady=15, padx=5, highlightbackground="gray", highlightthickness=1
        )
        search.columnconfigure(1, weight=1)
        search.rowconfigure(0, weight=1)
        self.other_name_lbl = Label(search, text="Figurinhas de: ")
        self.other_name_entry = Entry(search)
        self.other_name_entry.grid(column=1, row=0, sticky="we", padx=5)
        self.other_name_lbl.grid(row=0, column=0)
        self.search_btn = Button(search, text="Buscar", command=self._search_clicked)
        self.search_btn.bind("<Return>", self._search_clicked)
        self.search_btn.grid(column=2, row=0)
        search.grid(row=0, column=1, sticky="we")

        self.other_list = ListSticker(self)
        self.other_list.grid(row=1, column=1, sticky="snew")

        Button(self, text="Solicitar Troca", command=self._trade, padx=10).grid(
            row=2, column=0, columnspan=2, padx=10, pady=5
        )

        self.user = None

    def clear(self):
        self.my_list.clear()
        self.other_list.clear()
        self.other_name_entry.delete(0, END)

    def update_view(self):
        resp = requests.get(
            self.window.stickers_route + "/list",
            data=json.dumps(
                {"username": self.window.logged_user_username}, ensure_ascii=False
            ),
            headers=self.window.headers,
        ).json()

        self.clear()
        self.my_list.add_stickers(resp)

    def _search_clicked(self, event=None):
        self.other_list.clear()
        username = self.other_name_entry.get()

        if username == self.window.logged_user_username:
            # cant trade with myself
            return

        resp = requests.get(
            self.window.stickers_route + "/list",
            data=json.dumps({"username": username}, ensure_ascii=False),
            headers=self.window.headers,
        ).json()

        self.other_list.add_stickers(resp)

    def _trade(self):
        other_username = self.other_name_entry.get()
        my_stickers = self.my_list.get_selected_stickers()
        other_stickers = self.other_list.get_selected_stickers()

        data = {
            "my_stickers": my_stickers,
            "other_stickers": other_stickers,
            "my_username": self.window.logged_user_username,
            "other_username": other_username,
        }
        resp = requests.post(
            self.window.trade_route + "/request",
            data=json.dumps(data, ensure_ascii=False),
            headers=self.window.headers,
        ).json()

        if resp["status"]:
            self.window.show_page("homepage", menu=True)
        else:
            print("Error on trade")
