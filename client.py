from client.app import App
from client.trade import TradeView
from client.homepage import HomepageView
from client.login import LoginView
from client.register import RegisterView

if __name__ == "__main__":
    app = App()
    login = LoginView(app)
    register = RegisterView(app)
    homepage = HomepageView(app)
    trade = TradeView(app)

    app.add_page("login", login)
    app.add_page("register", register)
    app.add_page("homepage", homepage)
    app.add_page("trade", trade)

    app.show_page("login")
    
    app.mainloop()