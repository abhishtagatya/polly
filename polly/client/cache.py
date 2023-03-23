from typing import Optional

import redis


class CacheClient:

    ONE_MINUTE = 60
    ONE_HOUR = ONE_MINUTE * 60
    ONE_DAY = ONE_HOUR * 24
    ONE_WEEK = ONE_DAY * 7

    def __init__(self,
                 host: str,
                 port: int = 6732,
                 password: str = ''):
        self._host = host
        self._port = port
        self._password = password
        self._redis = redis.Redis(
            host=self._host,
            port=self._port,
            password=self._password
        )

    def get(self, key: str) -> Optional[str]:
        result = self._redis.get(key)
        if result is None:
            return
        return result.decode('utf-8')

    def set(self, key: str, value: str, ttl: int = 0):
        self._redis.set(key, value)
        if ttl != 0:
            self._redis.expire(key, ttl)
