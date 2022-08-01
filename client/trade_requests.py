from tkinter import *
from typing import List
from client.app import App
from models.domain import entity
from models.domain.entity import Status, Stickers
import json
import requests


class ItemListSticker(Frame):
    sticker: dict

    def __init__(self, window: Frame, sticker: dict):
        super().__init__(
            window, highlightbackground="gray", highlightthickness=1, pady=5
        )
        self.columnconfigure(2, weight=1)
        self.sticker = sticker

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


class TradeRequestsView(Frame):
    list_trades: List
    position: int

    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # header
        self.header = Label(self, text="Hello")
        self.header.grid(column=0, row=0, sticky="ew", padx=10, pady=10)

        # canvas
        self.content_frame = Frame(self)
        self.content_frame.grid(column=0, row=1, sticky="snew")
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)
        self.content_frame.rowconfigure(1, weight=1)

        # buttons
        self.buttons_frame = Frame(self, pady=10)
        self.buttons_frame.grid(column=0, row=2, sticky="ew")
        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.columnconfigure(1, weight=1)
        self.buttons_frame.columnconfigure(2, weight=1)
        self.buttons_frame.columnconfigure(3, weight=1)

        # create lists
        Label(self.content_frame, text="Figurinhas a receber", pady=10).grid(
            column=0, row=0
        )
        self.list_receive = ListSticker(self.content_frame)
        self.list_receive.grid(column=0, row=1, sticky="snew")

        Label(self.content_frame, text="Figurinhas a enviar", pady=10).grid(
            column=1, row=0
        )
        self.list_send = ListSticker(self.content_frame)
        self.list_send.grid(column=1, row=1, sticky="snew")

        # create buttons
        self.btn_next = Button(
            self.buttons_frame, text="Próximo", command=self._next_clicked
        )
        self.btn_next.grid(column=3, row=0, sticky="e", padx=10)
        self.btn_prev = Button(
            self.buttons_frame, text="Anterior", command=self._prev_clicked
        )
        self.btn_prev.grid(column=0, row=0, sticky="w", padx=10)
        self.btn_accept = Button(
            self.buttons_frame, text="Aceitar", command=self._accept_clicked
        )
        self.btn_accept.grid(column=2, row=0, sticky="w", padx=10)
        self.btn_recuse = Button(
            self.buttons_frame, text="Recusar", command=self._recuse_clicked
        )
        self.btn_recuse.grid(column=1, row=0, sticky="e", padx=10)

    def update_view(self, *args, **kwargs):
        resp = requests.get(
            self.window.trade_route + "/list",
            data=json.dumps(
                {"username": self.window.logged_user_username}, ensure_ascii=False
            ),
            headers=self.window.headers,
        ).json()

        self.position = 0
        self.list_trades = []
        for t in resp:
            self.list_trades.append(t)
        self.show()

    def _next_clicked(self, event=None):
        self.position += 1
        self.show()

    def _prev_clicked(self, event=None):
        self.position -= 1
        self.show()

    def _accept_clicked(self, event=None):
        trade = self.list_trades[self.position]

        # print(trade)

        resp = requests.post(
            self.window.trade_route + "/answer",
            data=json.dumps(
                {"trade_id": trade["trade_id"], "answer": True}, ensure_ascii=False
            ),
            headers=self.window.headers,
        ).json()

        if resp["status"]:
            print("stickers traded")
        else:
            print("something went wrong")

        self.update_view()

    def _recuse_clicked(self, event=None):
        trade = self.list_trades[self.position]

        resp = requests.post(
            self.window.trade_route + "/answer",
            data=json.dumps(
                {"trade_id": trade["trade_id"], "answer": False}, ensure_ascii=False
            ),
            headers=self.window.headers,
        ).json()

        if resp["status"]:
            print("trade recused")
        else:
            print("something went wrong")

        self.update_view()

    def show(self):
        if len(self.list_trades) == 0:
            self.header.config(text="Nenhuma Solicitação")
            self.btn_accept.config(state=DISABLED)
            self.btn_recuse.config(state=DISABLED)
            self.btn_prev.config(state=DISABLED)
            self.btn_next.config(state=DISABLED)
            self.list_receive.clear()
            self.list_send.clear()
        else:
            trade = self.list_trades[self.position]
            self.btn_accept.config(state=NORMAL)
            self.btn_recuse.config(state=NORMAL)

            if self.position == 0:
                self.btn_prev.config(state=DISABLED)
            else:
                self.btn_prev.config(state=NORMAL)

            if self.position == len(self.list_trades) - 1:
                self.btn_next.config(state=DISABLED)
            else:
                self.btn_next.config(state=NORMAL)

            self.header.config(text="Solicitação de " + trade["username"])

            self.list_receive.clear()
            self.list_receive.add_stickers(trade["to_receive"])

            self.list_send.clear()
            self.list_send.add_stickers(trade["to_send"])
