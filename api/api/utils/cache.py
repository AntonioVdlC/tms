import redis
from flask import current_app

r: redis.Redis = None


def init_cache():
    global r
    if r is None:
        current_app.logger.info("setting cache..")
        r = redis.Redis(host=current_app.config['REDIS_HOST'],
                        port=current_app.config['REDIS_PORT'],
                        db=current_app.config['REDIS_DB'])


def get_cache():
    global r
    return r
