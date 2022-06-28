from tkinter import *
from turtle import position
from typing import List
from client.app import App
from middleware.clientSocket import ClientSocket
from models.protocol.command import RequestTradesReceivedUserCommand, TradeItem


class RequestView(Frame):
    position: int
    user_id: int
    list_trades: List[TradeItem]

    def __init__(self, window: Frame):
        super().__init__(window)
        self.window = window
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.head = Label(self, text="Hello")
        self.head.grid(column=0, row=0, pady=20)

        self.btn_next = Button(self, text="Próxima", command=self._next_clicked)
        self.btn_next.grid(column=0, row=2, sticky="e", padx=20)
        self.btn_next.bind('<Return>', self._next_clicked)

    def update_view(self, *args, **kwargs):
        self.position = 0
        self.user_id = kwargs["user_id"]
        
        sock = ClientSocket()
        cmd = RequestTradesReceivedUserCommand(self.user_id)
        resp = sock.send_receive(cmd)

        self.list_trades = resp.trades

        if len(self.list_trades) == 0:
            self.head.config(text="Nenhuma solicitação")
        else:
            self.show_trade()

    def show_trade(self):
        trade = self.list_trades[self.position]
        self.head.config(text="Solicitação de " + trade.username_orig)

    def _next_clicked(self, event = None):
        if len(self.list_trades) == 0:
            return

        self.position = (self.position + 1) % len(self.list_trades)
        self.show_trade() 

    def clear(self):
        pass



class TradeRequestsView(Frame):
    view: RequestView

    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = Canvas(self)
        self.canvas.grid(column=0, row=0, sticky="snew")

        scroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scroll.grid(column=1, row=0, sticky="ns")

        self.canvas.configure(yscrollcommand=scroll.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox(ALL)))

        self.content = Frame(self.canvas, bg="red")
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)
        self.canvas_frame = self.canvas.create_window((0,0), window=self.content, anchor="nw")

        self.content.bind('<Configure>', self._frame_configure)
        self.canvas.bind('<Configure>', self._change_frame_width)

        self.request_view = RequestView(self.content)
        self.request_view.grid(column=0, row=0, sticky="snew")

    def update_view(self, *args, **kwargs):
        self.request_view.update_view(user_id=self.window.logged_user_id)

    def _change_frame_width(self, event):
        canvas_width = event.width
        canvas_height = event.height
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width, height=canvas_height)

    def _frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
