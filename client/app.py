from tkinter import *

import grpc

class App(Tk):
    logged_user_id: int

    def __init__(self):
        super().__init__()
        self.title("Troca de Figurinhas")
        self.geometry("800x500")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.pages = dict()
        self.cur_page = None
        self.logged_user_id = None
        self.logged_user_username = ""
        self.channel = grpc.insecure_channel("localhost:5555")
        

    def set_logged_user_id(self, user_id: int):
        self.logged_user_id = user_id

    def show_page(self, name: str, menu=False, *args, **kwargs):
        if self.cur_page:
            self.cur_page.grid_forget()
        self.cur_page = self.pages[name]
        self.cur_page.grid(column=0, row=0, sticky="snew")
        self.cur_page.update_view(*args, **kwargs)

        if menu:
            self._show_menu_bar()
        else:
            self._hide_menu_bar()

    def add_page(self, name: str, page: Frame):
        self.pages[name] = page

    def _hide_menu_bar(self):
        self.config(menu=Menu(self))

    def _show_menu_bar(self):
        self.menubar = Menu(self)
        self.menubar.add_command(label="inicio", command=lambda:self.show_page("homepage", menu=True))
        self.menubar.add_command(label="trocar", command=lambda:self.show_page("trade", menu=True))
        self.menubar.add_command(label="solicitações", command=lambda:self.show_page("trade_requests", menu=True))
        self.menubar.add_command(label="sair", command=lambda:self.show_page("login"))
        self.config(menu=self.menubar)