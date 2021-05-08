from flask import current_app
import mmh3

import json
import uuid

from api.utils.cache import get_cache
from api.models.user import User, get_user_by_id, get_users
from api.utils.app_wrapper import get_config


class InvalidNameException(ValueError):
    def __init__(self, value):
        self.value = value


class UserNotFoundException(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


def clear_user_cache(user_id: str):
    key = f'user_{user_id}'
    get_cache().delete(key)


def get_user(user_id: str) -> User:
    key = f'user_{user_id}'
    cached_user_str = get_cache().get(key)
    user: User = None
    if cached_user_str is None:
        user = get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        get_cache().setex(key, get_config()['CACHE_TTL_SECS'], json.dumps(user.as_dict(to_cache=True)))
    else:
        user_dict = json.loads(cached_user_str)
        user = User.from_dict(user_dict, from_cache=True)
    return user


def get_user_by_ids(user_ids: list) -> dict:
    keys = list(map(lambda i: f'user_{i}', user_ids))
    cached_user_str_list = [x for x in get_cache().mget(*keys) if x is not None]
    cached_users = list(map(lambda user_str: User.from_dict(json.loads(user_str),
                                                            from_cache=True),
                            cached_user_str_list))
    un_cached_user_ids = []
    cached_user_ids = set(map(lambda user: str(user.object_id), cached_users))
    for user_id in user_ids:
        if user_id not in cached_user_ids:
            un_cached_user_ids.append(user_id)
    un_cached_users = get_users(un_cached_user_ids)
    pipeline = get_cache().pipeline()
    for un_cached_user in un_cached_users:
        key = f'user_{str(un_cached_user.object_id)}'
        pipeline.setex(key, get_config()['CACHE_TTL_SECS'], json.dumps(un_cached_user.as_dict(to_cache=True)))
    pipeline.execute()
    users = cached_users + un_cached_users
    users_dict = dict((str(user.object_id), user) for user in users)
    return users_dict


def generate_unique_hash(user_info: str, hash128: bool = False) -> str:
    str_to_hash = "{user_info}|{uuid}".format(user_info=user_info, uuid=str(uuid.uuid4()))
    if hash128:
        return mmh3.hash128(str_to_hash, signed=False)
    else:
        return mmh3.hash(str_to_hash, signed=False)
