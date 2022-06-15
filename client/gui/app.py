from tkinter import *
from gui.register import RegisterFrame
from gui.homepage import HomepageFrame
from gui.login import LoginFrame

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Troca de Figurinhas")
        self.geometry("800x500")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.login_frame = LoginFrame(self)
        self.homepage_frame = HomepageFrame(self)
        self.register_frame = RegisterFrame(self)
        self.show_login()
        self.mainloop()

    def show_login(self):
        self.config(menu=Menu(self))
        self.login_frame.tkraise()

    def show_homepage(self):
        self.build_menu_bar()
        self.homepage_frame.tkraise()

    def show_register(self):
        self.register_frame.tkraise()

    def show_search(self):
        self.build_menu_bar()
        pass

    def show_exchange(self):
        self.build_menu_bar()
        pass

    def build_menu_bar(self):
        self.menubar = Menu(self)
        self.menubar.add_command(label="inicio", command=self.show_homepage)
        self.menubar.add_command(label="buscar", command=self.show_search)
        self.menubar.add_command(label="trocar", command=self.show_exchange)
        self.menubar.add_command(label="sair", command=self.show_login)
        self.config(menu=self.menubar)