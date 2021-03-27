import redis
from flask import current_app, g


def init_cache():
    if 'cache' not in g:
        r = redis.Redis(host=current_app.config['REDIS_HOST'],
                        port=current_app.config['REDIS_PORT'],
                        db=current_app.config['REDIS_DB'])
        g.cache = r
