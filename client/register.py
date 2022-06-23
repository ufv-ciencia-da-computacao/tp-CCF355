from cgitb import text
import json
from tkinter import *

from client.app import App
from middleware.clientSocket import ClientSocket
from models.protocol.command import RequestCreateUserCommand

class RegisterView(Frame):
    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        content = Frame(self)
        content.columnconfigure(0, weight=1)
        Label(content, text="Usuário:").grid(row=0, column=0, columnspan=2, sticky="w")
        self.username_input = Entry(content, width=40)
        self.username_input.grid(row=1, column=0, columnspan=2)
        Label(content, text="Senha:").grid(row=2, column=0, columnspan=2, sticky="w")
        self.password_input = Entry(content, show='*', width=40)
        self.password_input.grid(row=3, column=0, columnspan=2)
        Label(content, text="Confirmar senha:").grid(row=4, column=0, columnspan=2, sticky="w")
        self.confirm_input = Entry(content, show='*', width=40)
        self.confirm_input.grid(row=5, column=0, columnspan=2)
        self.error_msg_lbl = Label(content, fg="red")
        Button(content, text="Cancelar", command=self._cancel_clicked).grid(row=7, column=0, sticky="e", pady=10, padx=5)
        Button(content, text="Confirmar", command=self._confirm_clicked).grid(row=7, column=1, sticky="e", pady=10, padx=5)
        content.pack(expand=True)

        self.sock = ClientSocket()

    def clear(self):
        self.username_input.delete(0, END)
        self.password_input.delete(0, END)
        self.confirm_input.delete(0, END)
        self.error_msg_lbl.grid_forget()

    def _confirm_clicked(self):
        username = self.username_input.get()
        password = self.password_input.get()
        confirm = self.confirm_input.get()

        if len(username) == 0 or len(password) == 0 or len(confirm) == 0:
            self._show_error("Campos não preenchidos")
            return

        if password != confirm:
            self._show_error("Senhas diferentes")
            return

        sock = ClientSocket()
        cmd = RequestCreateUserCommand(username=username, password=password)
        resp = sock.send_receive(cmd)
        print(resp["message_type"])

        if resp["status"]:
            self.window.show_page("login")
        else:
            self._show_error("Falha ao cadastrar")

    def _show_error(self, msg: str):
        self.error_msg_lbl.grid_forget()
        self.error_msg_lbl.grid(row=6, column=0, sticky="w")
        self.error_msg_lbl.config(text=msg)

    def _cancel_clicked(self):
        print("go to login")
        self.window.show_page("login")