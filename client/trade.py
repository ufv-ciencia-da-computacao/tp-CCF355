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
from typing import Any, Callable, List
from middleware.clientSocket import ClientSocket
from models.domain.entity import Stickers, Users
from client.app import App
from models.protocol.command import RequestListStickersUserCommand, RequestTradeUserToUserCommand, RequestUserCommand

class ItemListSticker(Frame):
    sticker: Stickers

    def __init__(self, window: Frame, sticker: Stickers):
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
        Label(self, text=self.sticker.playername, padx=5).grid(
            row=0, column=2, sticky="w"
        )

        Label(self, text="País:", padx=5).grid(row=1, column=1, sticky="w")
        Label(self, text=self.sticker.country, padx=5).grid(row=1, column=2, sticky="w")

        Label(self, text="Raridade:", padx=5).grid(row=2, column=1, sticky="w")
        Label(self, text=str(self.sticker.rarity), padx=5).grid(
            row=2, column=2, sticky="w"
        )

    def is_selected(self):
        return self.selected.get()


class ListSticker(Frame):
    view_list: List[ItemListSticker]

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
                selected.append(item.sticker.id)
        return selected

    def update_view(self, *args, **kwargs):
        for v in self.view_list:
            v.pack_forget()
            v.destroy()
        self.view_list.clear()

    def add_stickers(self, stickers: List[Stickers]):
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
    user: Users

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
        sock = ClientSocket()
        cmd = RequestUserCommand(self.window.logged_user_id)
        resp = sock.send_receive(cmd)
        self.user = resp.user

        self.clear()
        self.my_list.add_stickers(self.user.stickers)

    def _search_clicked(self, event=None):
        self.other_list.clear()
        username = self.other_name_entry.get()

        if username == self.user.username:
            # cant trade with myself
            return

        sock = ClientSocket()
        cmd = RequestListStickersUserCommand(username=username)
        resp = sock.send_receive(cmd)

        self.other_list.add_stickers(resp.stickers)

    def _trade(self):
        my_stickers = self.my_list.get_selected_stickers()
        other_stickers = self.other_list.get_selected_stickers()

        sock = ClientSocket()
        cmd = RequestTradeUserToUserCommand(
            self.user.username, my_stickers, self.other_name_entry.get(), other_stickers
        )
        resp = sock.send_receive(cmd)
        print(resp)
