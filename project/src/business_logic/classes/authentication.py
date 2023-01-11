import os

from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from .jwt_manager import JWTManager


def provide_jwt_manager_instance():
    return JWTManager(int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]),
                      os.environ["SECRET"],
                      os.environ["ALGORITHM"])


class Authentication:
    def __init__(self):
        self.cryptography_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        )

    def get_hashed_password(self, password: str) -> str:
        return self.cryptography_context.hash(password)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return self.cryptography_context.verify(
            plain_password, hashed_password
        )

    def requires_authentication(
        self, jwt_manager: JWTManager = Depends(provide_jwt_manager_instance),
            auth: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ) -> None:
        return jwt_manager.decode_token(auth.credentials)
