from tkinter import *
from typing import List
from client.app import App
from models.domain.entity import Users

import grpc
from middleware.sticker_pb2 import ListStickersRequest
from middleware.sticker_pb2_grpc import StickerServiceStub, StickerServiceServicer
import service.StickerService

class StickerFrame(Frame):
    def __init__(self, window: Frame, playername: str,  country: str, rarity: int):
        super().__init__(window, width=200, height=330, pady=10, bg="#E5E7E9")
        self.pack_propagate(False)
        self.window = window

        self.columnconfigure(1, weight=1)

        self.image = Frame(self, bg="grey", width=180, height=180)
        self.grid_propagate(False)
        self.image.grid(row=0, column=0, pady=5, columnspan=2)

        Label(self, text="Nome: ", bg=self['bg']).grid(column=0, row=1, padx=10, sticky="w")
        self.playername = Label(self, text=playername, bg=self['bg'], wraplength=100, justify=LEFT)
        self.playername.grid(column=1, row=1, sticky="w")

        Label(self, text="País: ", bg=self['bg']).grid(column=0, row=2, padx=10, sticky="w")
        self.country = Label(self, text=country, bg=self['bg'], wraplength=100, justify=LEFT)
        self.country.grid(column=1, row=2, sticky="w", pady=5)

        Label(self, text="Raridade: ", bg=self['bg']).grid(column=0, row=3, padx=10, sticky="w")
        self.rarity = Label(self, text=str(rarity), bg=self['bg'], wraplength=100, justify=LEFT)
        self.rarity.grid(column=1, row=3, sticky="w")

class HomepageView(Frame):
    list_stickers : List[StickerFrame]
    user: Users

    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.welcome = Label(self, pady=10)
        self.welcome.grid(row=0, column=0)

        content = Frame(self)
        self.canvas = Canvas(content)
        self.canvas.pack(side="left", fill="both", expand=True)
        content.grid(row=1, column=0, sticky="snew")

        scroll = Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        scroll.grid(row=2, column=0, sticky="we")

        self.canvas.configure(xscrollcommand=scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox(ALL)))

        self.f = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.f, anchor="nw")

        self.list_stickers = []

        self.user = None

    def update_view(self, *args, **kwargs):
        self.welcome.config(text="Bem vindo " + self.window.logged_user_username)
        self.clear()

        stub = StickerServiceStub(channel=self.window.channel)
        resp = stub.list_stickers(ListStickersRequest(username=self.window.logged_user_username))
        for r in resp.sticker:
            print(r.playername, r.country, r.rarity, r.id)
            s = StickerFrame(self.f, r.playername, r.country, r.rarity)
            s.pack(side="left", padx=10)
            self.list_stickers.append(s)

    def clear(self):
        for s in self.list_stickers:
            s.grid_forget()
            s.destroy()
        self.list_stickers.clear()