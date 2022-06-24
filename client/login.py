from tkinter import *
from client.app import App
from middleware.clientSocket import ClientSocket
from models.domain.entity import Users
from models.protocol.command import RequestLoginCommand, ResponseLoginCommand
from models.protocol.socketio import ReaderResponse

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
        
        self.btn_enter = Button(content, text="Entrar", command=self._enter_clicked)
        self.btn_enter.grid(row=5, column=1, sticky="e", pady=10, padx=5)

        content.pack(expand=True)

    def update_view(self):
        self.username.delete(0, END)
        self.password.delete(0, END)


    def _show_error_msg(self):
        self.lbl_error.grid_forget()
        self.lbl_error.grid(row=4, column=0, sticky="w", columnspan=2)

    def _enter_clicked(self):
        username = self.username.get()
        password = self.password.get()

        sock = ClientSocket()
        cmd = RequestLoginCommand(username=username, password=password)
        resp = sock.send_receive(cmd)

        if resp.user.id != None:
            self.window.set_logged_user(resp.user)
            self.window.show_page("homepage", menu=True)

    def _register_clicked(self):
        print("register")
        self.window.show_page("register")