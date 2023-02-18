from fastapi.security import HTTPAuthorizationCredentials
from typing import Callable
from business_logic.authentication.auth import Authentication
from business_logic.authentication.jwt_manager import JWTManager


def check_auth() -> Callable[[JWTManager, HTTPAuthorizationCredentials], None]:
    return Authentication().requires_authentication
