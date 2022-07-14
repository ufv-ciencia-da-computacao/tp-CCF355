from models.domain import entity
from middleware.user_pb2 import LoginResponse, CreateResponse

from models.repository.repo import ListStickersRepository, StickersRepository, UsersRepository
from service.StickersPack import StickersPack
from middleware.user_pb2_grpc import UserServiceServicer

class UserService(UserServiceServicer):
    def __init__(self, us_repo : UsersRepository, s_repo : StickersRepository, ls_repo : ListStickersRepository) -> None:
        super().__init__()
        self.us_repo = us_repo
        self.stickers_pack = StickersPack(s_repo, ls_repo)
        
    def login(self, request, context):
        resp = LoginResponse(user_id=-1)
        user = self.us_repo.get(request.username)
        if user is not None and user.password == request.password:
            resp.user_id = user.id
            return resp
        raise

    def register(self, request, context):
        resp = CreateResponse(status=False)
        user = entity.Users(username=request.username, password=request.password)
        try:
            self.us_repo.add(user=user)
            self.stickers_pack.add_pack2user(
                user=self.us_repo.get(user.username)
            )
            resp.status = True
            print("ok")
        except Exception:
            pass
        
        return resp