from tkinter import *

class RegisterFrame(Frame):
    def __init__(self, window: Tk):
        super().__init__(window)
        self.grid(row=0, column=0, sticky="nsew")
        self.window = window
        self.container = Frame(self)
        self.container.columnconfigure(0, weight=1)
        Label(self.container, text="Usuário:").grid(row=0, column=0, columnspan=2, sticky="w")
        Entry(self.container, width=40).grid(row=1, column=0, columnspan=2)
        Label(self.container, text="Senha:").grid(row=2, column=0, columnspan=2, sticky="w")
        Entry(self.container, show='*', width=40).grid(row=3, column=0, columnspan=2)
        Label(self.container, text="Confirmar senha:").grid(row=4, column=0, columnspan=2, sticky="w")
        Entry(self.container, show='*', width=40).grid(row=5, column=0, columnspan=2)
        Button(self.container, text="Cancelar", command=self.cancel_btn_clicked).grid(row=6, column=0, sticky="e", pady=10, padx=5)
        Button(self.container, text="Confirmar", command=self.confirm_btn_clicked).grid(row=6, column=1, sticky="e", pady=10, padx=5)
        self.container.pack(expand=True)

    def confirm_btn_clicked(self):
        print("registered")
        pass

    def cancel_btn_clicked(self):
        self.window.show_login()