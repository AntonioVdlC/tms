import redis
from flask import current_app

_r: redis.Redis = None


def init_cache():
    global _r
    if _r is None:
        current_app.logger.info("Setting up cache..")
        _r = redis.Redis(host=current_app.config['REDIS_HOST'],
                         port=current_app.config['REDIS_PORT'],
                         db=current_app.config['REDIS_DB'])


def get_cache():
    global _r
    return _r
