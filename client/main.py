from app import App
from exchange import ExchangeView
from homepage import HomepageView
from login import LoginView
from register import RegisterView

if __name__ == "__main__":
    app = App()
    login = LoginView(app)
    register = RegisterView(app)
    homepage = HomepageView(app)
    exchange = ExchangeView(app)

    app.add_page("login", login)
    app.add_page("register", register)
    app.add_page("homepage", homepage)
    app.add_page("exchange", exchange)

    app.show_page("login")
    app.mainloop()