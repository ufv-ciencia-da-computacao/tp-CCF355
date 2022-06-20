from tkinter import *

from app import App

class RegisterView(Frame):
    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        content = Frame(self)
        content.columnconfigure(0, weight=1)
        Label(content, text="Usuário:").grid(row=0, column=0, columnspan=2, sticky="w")
        Entry(content, width=40).grid(row=1, column=0, columnspan=2)
        Label(content, text="Senha:").grid(row=2, column=0, columnspan=2, sticky="w")
        Entry(content, show='*', width=40).grid(row=3, column=0, columnspan=2)
        Label(content, text="Confirmar senha:").grid(row=4, column=0, columnspan=2, sticky="w")
        Entry(content, show='*', width=40).grid(row=5, column=0, columnspan=2)
        Button(content, text="Cancelar", command=self._cancel_clicked).grid(row=6, column=0, sticky="e", pady=10, padx=5)
        Button(content, text="Confirmar", command=self._confirm_clicked).grid(row=6, column=1, sticky="e", pady=10, padx=5)
        content.pack(expand=True)

    def _confirm_clicked(self):
        print("registered")
        pass

    def _cancel_clicked(self):
        print("go to login")
        self.window.show_page("login")