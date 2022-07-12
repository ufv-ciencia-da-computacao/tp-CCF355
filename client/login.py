from tkinter import *
from client.app import App

import grpc
from middleware.user_pb2_grpc import UserServiceStub
from middleware.user_pb2 import LoginRequest, LoginResponse

class LoginView(Frame):
    def __init__(self, window: App):
        super().__init__(window)
        self.window = window
        
        content = Frame(self)
        content.columnconfigure(0, weight=1)

        Label(content, text="Usuário:").grid(row=0, column=0, columnspan=2, sticky="w")
        
        self.username = Entry(content, width=40)
        self.username.grid(row=1, column=0, columnspan=2)
        
        Label(content, text="Senha:").grid(row=2, column=0, columnspan=2, sticky="w")
        
        self.password = Entry(content, show='*', width=40)
        self.password.grid(row=3, column=0, columnspan=2)
        
        self.lbl_error = Label(content, text="Usuário ou senha inválidos", fg="red")
        
        self.btn_register = Button(content, text="Cadastrar", command=self._register_clicked)
        self.btn_register.grid(row=5, column=0, sticky="e", pady=10, padx=5)
        self.btn_register.bind('<Return>', self._register_clicked)

        self.btn_enter = Button(content, text="Entrar", command=self._enter_clicked)
        self.btn_enter.grid(row=5, column=1, sticky="e", pady=10, padx=5)
        self.btn_enter.bind('<Return>', self._enter_clicked)

        content.pack(expand=True)

    def update_view(self, *args, **kwargs):
        self.username.delete(0, END)
        self.password.delete(0, END)
        self.username.focus()


    def _show_error_msg(self):
        self.lbl_error.grid_forget()
        self.lbl_error.grid(row=4, column=0, sticky="w", columnspan=2)

    def _enter_clicked(self, event = None):
        username = self.username.get()
        password = self.password.get()

        try:
            with grpc.insecure_channel('localhost:5555') as channel:
                stub = UserServiceStub(channel=channel)
                resp = stub.login(LoginRequest(username=username, password=password))
                self.window.username = username
                self.window.set_logged_user_id(user_id=resp.user_id)
                self.window.show_page("homepage", menu=True)
        except Exception:
            self._show_error_msg()  

    def _register_clicked(self, event = None):
        self.window.show_page("register")