from flask import current_app
from pydantic import BaseModel, EmailStr
import mmh3

import uuid
import json

from api.utils.db import get_db
from api.utils.cache import get_cache, get_token_generation_script
from api.models.user import User, get_user_by_email
from api.auth.exceptions import DuplicateSignupException, UnknownEmailException


class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class LoginRequest(BaseModel):
    email: EmailStr


class CallbackRequest(BaseModel):
    token: str
    operation: str


class AuthTokenResponse(BaseModel):
    token: str


def signup(request: SignupRequest):
    email = str(request.email)
    existing_user = get_user_by_email(email)
    if existing_user is None:
        token: str = generate_email_hash(email)
        set_token(email, token, json.dumps(request.dict()))
        signup_url = generate_callback_url(token, "signup")
        send_signup_email(signup_url)
        return {"message": "Please check email to complete sign up flow"}
    else:
        current_app.logger.warn(f"Already an existing user for: {email}")
        raise DuplicateSignupException(email)


def login(request: LoginRequest):
    current_app.logger.info('Logging in user: ' + request.email)
    email = str(request.email)
    user = get_user_by_email(email)
    if user is None:
        raise UnknownEmailException(email)
    else:
        token: str = generate_email_hash(email)
        set_token(email, token, json.dumps(user.to_dict()))
        login_url = generate_callback_url(token, "login")
        send_login_email(login_url)
        return {"message": "Please check email to login"}


def callback(request: CallbackRequest) -> AuthTokenResponse:
    current_app.logger.info(f'Completing auth flow for token: {request.token}')
    return AuthTokenResponse(token="token")


def generate_email_hash(email: str) -> str:
    str_to_hash = "{email}|{uuid}".format(email=email, uuid=str(uuid.uuid4()))
    return mmh3.hash(str_to_hash, signed=False)


def set_token(email: str, token: str, user_info: str):
    script = get_token_generation_script()
    ttl: int = int(current_app.config['SIGNUP_TTL_SECS'])
    current_app.logger.info(f'email: {email}, token: {token}, user_info: {user_info}, ttl: {ttl}')
    script(keys=[email, token], args=[token, user_info, ttl])


def generate_callback_url(token: str, operation: str) -> str:
    url = '{base_url}/auth/callback?token={token}&operation={operation}' \
        .format(base_url=current_app.config['TMS_BASE_URL'], operation=operation, token=token)
    return url


def send_signup_email(signup_url: str):
    # TODO: send email using flask email and jinja templates. its all yours antonio :hugging_face:
    current_app.logger.info(f'Sending email for url: {signup_url}')


def send_login_email(login_url: str):
    # TODO: send email using flask email and jinja templates. its all yours antonio :hugging_face:
    current_app.logger.info(f'Sending email for url: {login_url}')
