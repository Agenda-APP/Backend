from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException


class JWTManager:
    def __init__(self, access_token_expire_minutes, secret, algorithm):
        self.secret = secret
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, email: str):
        payload = {
            "exp": datetime.utcnow()
            + timedelta(minutes=self.access_token_expire_minutes),
            "iat": datetime.utcnow(),
            "sub": email,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> None:
        try:
            jwt.decode(
                token, self.secret, algorithms=[self.algorithm]
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Signature has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
