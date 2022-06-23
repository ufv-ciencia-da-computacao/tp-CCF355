from middleware.clientSocket import ClientSocket
from models.protocol import command


if __name__ == "__main__":
    cs = ClientSocket()
    data = cs.send_receive(command.RequestCreateUserCommand("fredb26", "frederico"))
    print(data)

# if __name__ == "__main__":
