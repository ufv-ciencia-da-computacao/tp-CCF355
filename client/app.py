from tkinter import *

from sqlalchemy import column

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Troca de Figurinhas")
        self.geometry("800x500")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.pages = dict()
        self.cur_page = None

    def show_page(self, name: str, menu=False):
        if self.cur_page:
            self.cur_page.grid_forget()
        self.cur_page = self.pages[name]
        self.cur_page.grid(column=0, row=0, sticky="snew")
        self.cur_page.clear()

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
        self.menubar.add_command(label="buscar", command=lambda:self.show_page("search", menu=True))
        self.menubar.add_command(label="trocar", command=lambda:self.show_page("exchange", menu=True))
        self.menubar.add_command(label="sair", command=lambda:self.show_page("login"))
        self.config(menu=self.menubar)