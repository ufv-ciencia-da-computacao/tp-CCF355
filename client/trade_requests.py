from tkinter import *
from typing import List
from client.app import App
from middleware.clientSocket import ClientSocket
from models.domain.entity import TradeRequest, Users
from models.protocol.command import RequestUserCommand


class RequestView(Frame):

    position: int

    def __init__(self, window: Frame, user_id: int):
        super().__init__(window)
        self.window = window
        self.rowconfigure(1, weight=1)

        self.head = Label(self)
        self.head.grid(column=0, row=0, sticky="we")

        self.btn_next = Button(self, text="Próxima", command=self._next_clicked)
        self.btn_next.grid(column=0, row=2, sticky="e")
        self.btn_next.bind('<Return>', self._next_clicked)

    def update_view(self):
        pass

    def _next_clicked(self, event = None):
        if len(self.list_requests) == 0:
            return
        self.position = (self.position + 1) % len(self.list_requests)
        self.update()
    
    def add_requests(self, requests = None):
        pass

    def clear(self):
        for v in self.list_requests:
            v.pack_forget()
            v.destroy()
        self.list_requests.clear()



class TradeRequestsView(Frame):
    # list_requests:
    position: int
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

        self.content = Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0,0), window=self.content, anchor="nw")

        self.content.bind('<Configure>', self._frame_configure)
        self.canvas.bind('<Configure>', self._change_frame_width)

        self.user = None
        self.list_requests = []

        self.request_view = RequestView(self.content, self.window.logged_user_id)
        self.request_view.pack(fill="x", expand=True)

    def update_view(self, *args, **kwargs):
        self.request_view.update_view()

    def _change_frame_width(self, event):
        canvas_width = event.width
        canvas_height = event.height
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width, height=canvas_height)

    def _frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
