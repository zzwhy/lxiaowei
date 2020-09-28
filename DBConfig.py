

import redis
from settings import REDIS_INI

class RedisConfig:

    rc = redis.Redis(
        host=REDIS_INI['host'],
        port=REDIS_INI['port'],
        decode_responses=REDIS_INI['decode_responses'],
        db=REDIS_INI['db']
    )
    @staticmethod
    def cache_keep(flag:bool):
        if flag:
            pass
        else:
            RedisConfig.rc.delete('fingers', 'links')