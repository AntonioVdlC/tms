from flask import current_app, g
from pydantic import BaseModel, validator, EmailStr
from pymongo.errors import PyMongoError, WriteError
from redis.exceptions import RedisError, ConnectionError

import json
from datetime import datetime
from enum import Enum

from api.utils.cache import get_cache, get_update_email_script
from api.user.exceptions import *
from api.commons import user as user_commons
from api.commons import organisation as organisation_commons
from api.commons import common as common
from api.models import user as user_db


class UserModel(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime


class UpdateDetailsRequest(BaseModel):
    first_name: str
    last_name: str

    @validator('first_name')
    def validate_first_name(cls, v):
        if '$' in v:
            raise user_commons.InvalidNameException(v)
        return v

    @validator('last_name')
    def validate_last_name(cls, v):
        if '$' in v:
            raise user_commons.InvalidNameException(v)
        return v


class UpdateEmailRequest(BaseModel):
    email: EmailStr


class UpdateEmailType(str, Enum):
    old = 'old'
    new = 'new'


class UpdateEmailCallback(BaseModel):
    token: str
    email_type: UpdateEmailType

    class Config:
        use_enum_values = True


def get_user(user_id: str) -> UserModel:
    try:
        user = user_commons.get_user(user_id)
        return UserModel(id=str(user.object_id), first_name=user.first_name, last_name=user.last_name, email=user.email,
                         created_at=user.created_at, updated_at=user.updated_at)
    except (PyMongoError, RedisError, ConnectionError) as e:
        raise common.UnknownSystemException(user_id)


def update_user_details(user_id: str, request: UpdateDetailsRequest) -> UserModel:
    try:
        existing_user = user_commons.get_user(user_id)
        first_name = request.first_name.strip()
        last_name = request.last_name.strip()
        update_result = user_db.update_user_details(user_id, first_name, last_name)
        if update_result.modified_count != 1:
            raise common.UnknownSystemException(user_id)
        user_commons.clear_user_cache(user_id)
        updated_user = user_commons.get_user(user_id)
        return UserModel(first_name=updated_user.first_name, last_name=updated_user.last_name, email=updated_user.email,
                         created_at=updated_user.created_at, updated_at=updated_user.updated_at)
    except (PyMongoError, RedisError, ConnectionError) as e:
        raise common.UnknownSystemException(user_id)


def update_user_email(user_id: str, request: UpdateEmailRequest):
    try:
        user = user_commons.get_user(user_id)
        new_email = str(request.email)
        prev_update_email_info = get_update_email_cache(user_id)
        if prev_update_email_info is None:
            user_for_new_email = user_db.get_user_by_email(new_email)
            if user_for_new_email is None:
                old_email_token: str = user_commons.generate_unique_hash(user.email)
                new_email_token: str = user_commons.generate_unique_hash(new_email)
                update_user_dict = {"id": user_id, "old_email": user.email, "old_email_token": old_email_token,
                                    "new_email": new_email, "new_email_token": new_email_token}
                set_update_email_cache(user_id, update_user_dict)
                old_email_url = generate_callback_url(old_email_token, UpdateEmailType.old.value)
                new_email_url = generate_callback_url(new_email_token, UpdateEmailType.new.value)
                current_app.logger.info(f'Old email url: {old_email_url}')
                current_app.logger.info(f'new email url: {new_email_url}')
                send_update_email_old(user.email, old_email_url)
                send_update_email_new(new_email, new_email_url)
                return {"message": "Emails sent for updating user email"}
            else:
                raise DuplicateEmailException(str(request.email))
        else:
            if prev_update_email_info['new_email'] == new_email:
                return {"message": "Email has been sent for update"}
            else:
                raise DuplicateUpdateRequestException(new_email)
    except (PyMongoError, RedisError, ConnectionError) as e:
        raise common.UnknownSystemException(user_id)


def update_user_email_callback(user_id: str, request: UpdateEmailCallback):
    try:
        user = user_commons.get_user(user_id)
        update_email_info = get_update_email_cache(user_id)
        if update_email_info is None:
            raise UnknownUpdateEmailException(user_id)
        else:
            current_app.logger.info(f'info: {update_email_info}')
            new_email = update_email_info['new_email']
            if request.email_type == UpdateEmailType.old:
                key = str(update_email_info['old_email_token'])
                other_key = str(update_email_info['new_email_token'])
                other_email = str(update_email_info['old_email'])
            elif request.email_type == UpdateEmailType.new:
                key = str(update_email_info['new_email_token'])
                other_key = str(update_email_info['old_email_token'])
                other_email = str(update_email_info['new_email'])
            else:
                raise UnknownEmailTypeException(request.token, request.email_type.value)

            current_app.logger.info(f'key: {key}, other key: {other_key}, request token: {request.token}')
            if key != request.token:
                current_app.logger.error('Illegal token..')
                raise IllegalUpdateTokenException(request.token)

            status = update_and_get_other_key_status(key, other_key)
            if status:
                current_app.logger.info('Received callbacks from both emails.. proceeding to update email')
                update_result = user_db.update_user_email(user_id, new_email)
                if update_result.modified_count != 1:
                    current_app.logger.error('did not update')
                    raise common.UnknownSystemException(user_id)

                user_commons.clear_user_cache(user_id)
                clear_update_email_cache(user_id,
                                         str(update_email_info['old_email_token']),
                                         str(update_email_info['new_email_token']))
                updated_user = user_commons.get_user(user_id)
                return UserModel(id=str(updated_user.object_id), first_name=updated_user.first_name,
                                 last_name=updated_user.last_name, email=updated_user.email,
                                 created_at=updated_user.created_at, updated_at=updated_user.updated_at).dict()
            else:
                return {"message": f"Received confirmation. Please double confirm from {other_email}"}
    except (PyMongoError, RedisError, ConnectionError) as e:
        current_app.logger.exception('everything is wrong bro', extra={'stack': True})
        raise common.UnknownSystemException(user_id)


def delete_user(user_id: str, token: str):
    try:
        user = user_commons.get_user(user_id)
        # TODO: figure out how to delete user in all organisations and what to do when user is admin/owner for one
        hashed_email = str(user_commons.generate_unique_hash(user.email, hash128=True))
        hashed_last_name = str(user_commons.generate_unique_hash(user.last_name, hash128=True))
        update_result = user_db.soft_delete_user(user_id, hashed_email, hashed_last_name)
        if update_result.modified_count != 1:
            raise common.UnknownSystemException(user_id)
        delete_auth_token(token)
        user_commons.clear_user_cache(user_id)
    except (PyMongoError, RedisError, ConnectionError) as e:
        current_app.logger.exception('everything is wrong bro', extra={'stack': True})
        raise common.UnknownSystemException(user_id)


def set_update_email_cache(user_id, update_user_dict):
    key = f'update_email_{user_id}'
    get_cache().setex(key, current_app.config['UPDATE_EMAIL_TTL_SECS'], json.dumps(update_user_dict))


def get_update_email_cache(user_id) -> dict:
    key = f'update_email_{user_id}'
    cache_response = get_cache().get(key)
    if cache_response is not None:
        cache_response = json.loads(cache_response)
    return cache_response


def generate_callback_url(token, email_type) -> str:
    base_url = current_app.config['TMS_BASE_URL']
    url = f'{base_url}/user/update/callback?token={token}&type={email_type}'
    return url


def send_update_email_old(old_email: str, old_url: str):
    current_app.logger.info('Sending email to old email')
    # TODO: antonio does his magic


def send_update_email_new(new_email: str, new_url: str):
    current_app.logger.info('Sending email to old email')
    # TODO: antonio does his magic


def update_and_get_other_key_status(key: str, other_key: str) -> bool:
    script = get_update_email_script()
    ttl: int = current_app.config['UPDATE_EMAIL_TTL_SECS']
    return script(keys=[key, other_key], args=[ttl, 1])


def clear_update_email_cache(user_id: str, old_token: str, new_token: str):
    update_email_key = f'update_email_{user_id}'
    delete_keys = [update_email_key, old_token, new_token]
    get_cache().delete(*delete_keys)


def delete_auth_token(token: str):
    get_cache().delete(token)


