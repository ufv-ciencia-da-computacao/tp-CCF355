from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
from sqlalchemy.orm import sessionmaker, scoped_session

from service.StickerService import StickerService
from service.UserService import UserService
from service.TradeService import TradeService
from base64 import b64encode

con = SQLiteConnection.get_connection(AlbumCredentials.host)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=con))

s_repo = repo.StickersRepository(session)
ls_repo = repo.ListStickersRepository(session)
us_repo = repo.UsersRepository(session)
t_repo = repo.TradeRepository(session)
ts_repo = repo.TradeStickersRepository(session)

sticker_service = StickerService(us_repo)
user_service = UserService(us_repo=us_repo, s_repo=s_repo, ls_repo=ls_repo)
trade_service = TradeService(
    ls_repo=ls_repo, us_repo=us_repo, t_repo=t_repo, ts_repo=ts_repo
)

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.post("/users/register")
def register():
    content = request.json
    username = content["username"]
    password = content["password"]

    status = user_service.register(username, password)

    return jsonify({"status": status})


@app.get("/users/login")
def login():
    content = request.json
    username = content["username"]
    password = content["password"]

    user_id = user_service.login(username, password)

    return jsonify({"user_id": user_id})


@app.get("/stickers/list")
def list_stickers():
    content = request.json
    username = content["username"]
    list_stickers = sticker_service.list_stickers(username)

    for l in list_stickers:
        l["photo"] = b64encode(l["photo"]).decode("utf-8")

    return jsonify(list_stickers)


@app.post("/trades/request")
def trade_stickers():
    content = request.json

    my_username = content["my_username"]
    other_username = content["other_username"]
    my_stickers = content["my_stickers"]
    other_stickers = content["other_stickers"]

    status = trade_service.request_trade(
        my_username, other_username, my_stickers, other_stickers
    )
    return jsonify({"status": status})


@app.get("/trades/list")
def list_trades():
    content = request.json
    username = content["username"]

    return jsonify(trade_service.get_trades(username=username))


@app.post("/trades/answer")
def response_trade():
    content = request.json
    trade_id = content["trade_id"]
    answer_trade = content["answer"]

    status = trade_service.answer_trade(trade_id=trade_id, accept=answer_trade)
    return jsonify({"status": status})
