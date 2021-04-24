from flask import current_app

import json

from api.utils.cache import get_cache
from api.models.user import User, get_user_by_id


def clear_user_cache(user_id: str):
    key = f'user_{user_id}'
    get_cache().delete(key)


def get_user(user_id: str) -> User:
    key = f'user_{user_id}'
    cached_user_str = get_cache().get(key)
    user: User = None
    if cached_user_str is None:
        user = get_user_by_id(user_id)
        get_cache().setex(key, current_app.config['CACHE_TTL_SECS'], json.dumps(user.as_dict(to_cache=True)))
    else:
        user_dict = json.loads(cached_user_str)
        user = User.from_dict(user_dict, from_cache=True)
    return user
