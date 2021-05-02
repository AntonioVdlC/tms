from flask import current_app, g
from pydantic import BaseModel, validator, EmailStr
from pymongo.errors import PyMongoError, WriteError
from redis.exceptions import RedisError, ConnectionError

import json
from datetime import datetime

from api.utils.cache import get_cache
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


def get_user(user_id: str) -> UserModel:
    try:
        user = user_commons.get_user(user_id)
        return UserModel(id=str(user.object_id),first_name=user.first_name, last_name=user.last_name, email=user.email,
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




