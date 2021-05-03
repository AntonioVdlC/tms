import redis
from flask import current_app

_r: redis.Redis = None
_token_generation_script: redis.client.Script = None
_update_email_script: redis.client.Script = None


def init_cache():
    global _r
    global _token_generation_script
    global _update_email_script
    if _r is None:
        current_app.logger.info("Setting up cache..")
        _r = redis.Redis(host=current_app.config['REDIS_HOST'],
                         port=current_app.config['REDIS_PORT'],
                         db=current_app.config['REDIS_DB'],
                         decode_responses=True)

        token_generation_lua = """
        local old_token = redis.call('GET', KEYS[1])
        if old_token then
            redis.call('DEL', old_token)
        end
        redis.call('SETEX', KEYS[1], ARGV[3], ARGV[1])
        redis.call('SETEX', KEYS[2], ARGV[3], ARGV[2])
        return ARGV[1]
        """
        _token_generation_script = _r.register_script(script=token_generation_lua)

        update_email_lua = """
        redis.call('SETEX', KEYS[1], ARGV[1], ARGV[2])
        return redis.call('EXISTS', KEYS[2])
        """
        _update_email_script = _r.register_script(script=update_email_lua)


def get_cache() -> redis.Redis:
    global _r
    return _r


def get_token_generation_script() -> redis.client.Script:
    global _token_generation_script
    return _token_generation_script


def get_update_email_script() -> redis.client.Script:
    global _update_email_script
    return _update_email_script

