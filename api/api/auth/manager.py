from pydantic import BaseModel, EmailStr, validator
from pymongo.errors import DuplicateKeyError, WriteError, PyMongoError
from redis.exceptions import ConnectionError, TimeoutError, RedisError

import uuid
import json
from enum import Enum

from api.utils.cache import get_cache, get_token_generation_script
from api.utils.db import get_client
from api.utils.app_wrapper import get_config, get_logger
from api.models import user as user_db
from api.models import organisation as organisation_db
from api.models import invite as invite_db
from api.auth.exceptions import *
from api.commons.user import InvalidNameException, UserNotFoundException, generate_unique_hash
from api.commons import organisation as organisation_commons
from api.commons import common as common


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
    try:
        email = str(request.email)
        existing_user = user_db.get_user_by_email(email)
        if existing_user is None:
            token: str = generate_unique_hash(email)
            set_token(email, token, json.dumps(request.dict()))
            signup_url = generate_callback_url(token, Operation.signup.value)
            send_signup_email(signup_url)
            return {"message": "Please check email to complete sign up flow"}
        else:
            get_logger().warn(f"Already an existing user for: {email} with id: {existing_user.object_id}")
            raise DuplicateSignupException(email)
    except (RedisError, ConnectionError) as e:
        raise common.UnknownAuthException()


def login(request: LoginRequest):
    try:
        get_logger().info('Logging in user: ' + request.email)
        email = str(request.email)
        user = user_db.get_user_by_email(email)
        if user is None:
            raise UnknownEmailException(email)
        else:
            token: str = generate_unique_hash(email)
            user_dict = user.as_dict(to_cache=True)
            set_token(email, token, json.dumps(user_dict))
            login_url = generate_callback_url(token, Operation.login.value)
            send_login_email(login_url)
            return {"message": "Please check email to login"}
    except (RedisError, ConnectionError) as e:
        raise common.UnknownAuthException()


def callback(request: CallbackRequest) -> AuthTokenResponse:
    try:
        get_logger().info(f'Completing auth flow for token: {request.token}, operation: {request.operation}')
        user_info = get_auth_user_info(request.token)
        if user_info is None:
            raise InvalidTokenException(request.token)
        else:
            user_id: str = None
            email: str = user_info['email']
            if request.operation == Operation.signup:
                try:
                    user = user_db.insert_user(user_info['email'], user_info['first_name'], user_info['last_name'])
                except DuplicateKeyError as e:
                    get_logger().warn(f"signup request attempted for an existing email: {email}")
                    raise DuplicateSignupException(email)
                user_id = str(user.object_id)
                # TODO: run through invites and add user to all organisations
                invites = invite_db.get_invites_by_email(email)
                if len(invites) > 0:
                    org_ids = []
                    invite_ids = []
                    with get_client().start_session() as session:
                        with session.start_transaction():
                            for invite in invites:
                                organisation_db.add_member_to_organisation(invite.org_id, user_id,
                                                                           invite.member_type, session)
                                org_ids.append(invite.org_id)
                                invite_db.soft_delete_invite(invite.object_id, session)
                            user_db.add_organisations_to_user(user_id, org_ids, session)
                            get_logger().info(f'invite ids: {invite_ids}, org_ids: {org_ids}')

                    organisation_commons.clear_orgs_cache(org_ids)
                else:
                    get_logger().info(f'No pending invites for {email}')
            elif request.operation == Operation.login:
                try:
                    user_id = str(user_info['_id'])
                except KeyError as e:
                    raise InvalidOperationException("Not a login token")
            else:
                raise InvalidOperationException(f'Unknown operation: {request.operation}')
            auth_token = str(uuid.uuid4())
            get_logger().info(f"auth_token: {auth_token}, object_id: {user_id}")
            set_auth_token(auth_token, user_id)
            delete_token_email(email, request.token)
            return AuthTokenResponse(token=auth_token)
    except (RedisError, ConnectionError) as e:
        raise common.UnknownAuthException()


def logout(token: str):
    try:
        get_cache().delete(token)
    except (ConnectionError, TimeoutError) as e:
        get_logger().error(f"Issue logging out with token: {token}")
        raise common.UnknownAuthException()


def set_token(email: str, token: str, user_info: str):
    script = get_token_generation_script()
    ttl: int = int(get_config()['SIGNUP_TTL_SECS'])
    get_logger().info(f'email: {email}, token: {token}, user_info: {user_info}, ttl: {ttl}')
    script(keys=[email, token], args=[token, user_info, ttl])


def generate_callback_url(token: str, operation: str) -> str:
    url = '{base_url}/auth/callback?token={token}&operation={operation}' \
        .format(base_url=get_config()['TMS_BASE_URL'], operation=operation, token=token)
    return url


def send_signup_email(signup_url: str):
    # TODO: send email using flask email and jinja templates. its all yours antonio :hugging_face:
    get_logger().info(f'Sending email for url: {signup_url}')


def send_login_email(login_url: str):
    # TODO: send email using flask email and jinja templates. its all yours antonio :hugging_face:
    get_logger().info(f'Sending email for url: {login_url}')


def get_auth_user_info(token: str):
    user_info = get_cache().get(token)
    if user_info is not None:
        user_info = json.loads(user_info)
    return user_info


def set_auth_token(token: str, user_id: str):
    get_cache().setex(token, get_config()['SESSION_TTL_SECS'], user_id)


def delete_token_email(email: str, token: str):
    get_cache().delete(email, token)
