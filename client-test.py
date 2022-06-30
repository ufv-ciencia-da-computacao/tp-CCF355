from middleware.clientSocket import ClientSocket
from models.protocol.command import RequestAnswerTradeCommand

sock = ClientSocket()
cmd = RequestAnswerTradeCommand(trade_id=8, accept=True)
resp = sock.send_receive(cmd)
# print(resp.as_dict())
