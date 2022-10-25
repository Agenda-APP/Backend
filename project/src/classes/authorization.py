import os
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext


class Authorization:
    def __init__(self):
        self.secret = os.environ["SECRET"]
        self.algorithm = os.environ["ALGORITHM"]
        self.access_token_expire_minutes = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
        self.cryptography_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()

    def get_hashed_password(self, password: str) -> str:
        return self.cryptography_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.cryptography_context.verify(plain_password, hashed_password)

    def create_access_token(self, email: str):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes),
            "iat": datetime.utcnow(),
            "sub": email
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def requires_authentication(self, auth: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> str:
        return self.decode_token(auth.credentials)
