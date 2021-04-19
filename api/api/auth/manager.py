from flask import current_app
from pydantic import BaseModel, EmailStr, validator
import mmh3
from pymongo.errors import DuplicateKeyError
from redis.exceptions import ConnectionError, TimeoutError

import uuid
import json
from enum import Enum

from api.utils.cache import get_cache, get_token_generation_script
from api.models.user import get_user_by_email, insert_user
from api.auth.exceptions import *


class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    @validator('first_name')
    def validate_first_name(cls, v):
        if '$' in v:
            raise InvalidNameException(v)
        return v

    @validator('last_name')
    def validate_last_name(cls, v):
        if '$' in v:
            raise InvalidNameException(v)
        return v


class LoginRequest(BaseModel):
    email: EmailStr


class Operation(str, Enum):
    signup = 'signup'
    login = 'login'


class CallbackRequest(BaseModel):
    token: str
    operation: Operation

    class Config:
        use_enum_values = True


class AuthTokenResponse(BaseModel):
    token: str


def signup(request: SignupRequest):
    email = str(request.email)
    existing_user = get_user_by_email(email)
    if existing_user is None:
        token: str = generate_email_hash(email)
        set_token(email, token, json.dumps(request.dict()))
        signup_url = generate_callback_url(token, Operation.signup.value)
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
        login_url = generate_callback_url(token, Operation.login.value)
        send_login_email(login_url)
        return {"message": "Please check email to login"}


def callback(request: CallbackRequest) -> AuthTokenResponse:
    current_app.logger.info(f'Completing auth flow for token: {request.token}, operation: {request.operation}')
    user_info = get_auth_user_info(request.token)
    if user_info is None:
        raise InvalidTokenException(request.token)
    else:
        user_id: str = None
        email: str = user_info['email']
        if request.operation == Operation.signup:
            try:
                user = insert_user(user_info['email'], user_info['first_name'], user_info['last_name'])
            except DuplicateKeyError as e:
                current_app.logger.warn(f"signup request attempted for an existing email: {email}")
                raise DuplicateSignupException(email)
            user_id = str(user.object_id)
        elif request.operation == Operation.login:
            try:
                user_id = str(user_info['object_id'])
            except KeyError as e:
                raise InvalidOperationException("Not a login token")
        else:
            raise InvalidOperationException(f'Unknown operation: {request.operation}')
        auth_token = str(uuid.uuid4())
        current_app.logger.info(f"auth_token: {auth_token}, object_id: {user_id}")
        set_auth_token(auth_token, user_id)
        delete_token_email(email, request.token)
        return AuthTokenResponse(token=auth_token)


def logout(token: str):
    try:
        get_cache().delete(token)
    except (ConnectionError, TimeoutError) as e:
        raise LogoutException(token)


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


def get_auth_user_info(token: str):
    user_info = get_cache().get(token)
    if user_info is not None:
        user_info = json.loads(user_info)
    return user_info


def set_auth_token(token: str, user_id: str):
    get_cache().setex(token, current_app.config['SESSION_TTL_SECS'], user_id)


def delete_token_email(email: str, token: str):
    get_cache().delete(email, token)
