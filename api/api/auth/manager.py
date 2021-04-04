from flask import current_app
from pydantic import BaseModel, EmailStr

from api.utils.db import get_db
from api.utils.cache import get_cache


class LoginRequest(BaseModel):
    email: EmailStr


class LoginResponse(BaseModel):
    token: str


def login(request: LoginRequest) -> LoginResponse:
    current_app.logger.info('Logging in user: ' +    request.email)
    return LoginResponse(token="token")