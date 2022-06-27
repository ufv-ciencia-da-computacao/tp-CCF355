from tkinter import *
from typing import List
from client.app import App
from middleware.clientSocket import ClientSocket
from models.domain.entity import TradeSticker, Users
from models.protocol.command import RequestUser


class ListRequestsView(Frame):
    def __init__(self, window: Frame):
        super().__init__(window)
        self.window = window

    def add_requests(self, requests: List[TradeSticker]):
        print(len(requests))

    def clear(self):
        pass


class TradeRequestsView(Frame):
    list_requests: ListRequestsView
    user: Users

    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        canvas = Canvas(self)
        canvas.grid(column=0, row=0, sticky="snew")

        scroll = Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll.grid(column=1, row=0, sticky="ns")

        canvas.configure(yscrollcommand=scroll.set)
        canvas.config(scrollregion=canvas.bbox(ALL))

        f = Frame(canvas)
        canvas.create_window((0, 0), window=f, anchor="nw")

        self.list_requests = ListRequestsView(f)

        self.user = None

    def update_view(self, *args, **kwargs):
        sock = ClientSocket()
        cmd = RequestUser(self.window.logged_user_id)
        resp = sock.send_receive(cmd)
        self.user = resp.user

        self.list_requests.clear()
        self.list_requests.add_requests(self.user.trades_received)
