from tkinter import *

class LoginFrame(Frame):
    def __init__(self, window: Tk):
        super().__init__(window)
        self.window = window
        self.grid(row=0, column=0, sticky="nsew")

        self.container = Frame(self)
        self.container.columnconfigure(0, weight=1)
        Label(self.container, text="Usuário:").grid(row=0, column=0, columnspan=2, sticky="w")
        Entry(self.container, width=40).grid(row=1, column=0, columnspan=2)
        Label(self.container, text="Senha:").grid(row=2, column=0, columnspan=2, sticky="w")
        Entry(self.container, show='*', width=40).grid(row=3, column=0, columnspan=2)
        Button(self.container, text="Cadastrar", command=self.register_btn_clicked).grid(row=4, column=0, sticky="e", pady=10, padx=5)
        Button(self.container, text="Entrar", command=self.enter_btn_clicked).grid(row=4, column=1, sticky="e", pady=10, padx=5)
        self.container.pack(expand=True)

    def enter_btn_clicked(self):
        print("signin")
        self.window.show_homepage()

    def register_btn_clicked(self):
        print("signup")
        self.window.show_register()