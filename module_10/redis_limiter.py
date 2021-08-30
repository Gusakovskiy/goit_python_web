from typing import Optional

from redis import RedisError

from module_10.redis_client import client


class RedisRateLimitException(Exception):
    pass


class RedisRateLimiter:
    """
        https://redislabs.com/redis-best-practices/basic-rate-limiting/
    """
    def __init__(self, limit: int, expire: int, prefix: str):
        """

        :param limit: max number of hit key can achieve
        :param expire: number of seconds in which key will expire
        """
        self.client = client
        self.limit = limit
        self.expire = expire
        self._separator = ';'
        self._prefix = prefix

    def _get_key(self, key) -> str:
        return f'{self._prefix}{self._separator}{key}'

    def _check_formatted_key(self, formatted_key: str):
        if not formatted_key.startswith(self._prefix):
            raise RedisRateLimitException(
                f'Wrong key format expect prefix:'
                f'{self._prefix} got {formatted_key}]'
            )

    def _get_counter(self, formatted_key: str) -> Optional[int]:
        self._check_formatted_key(formatted_key)
        value = self.client.get(formatted_key)
        return int(value) if value is not None else None

    def _increment_counter(self, formatted_key: str) -> None:
        self._check_formatted_key(formatted_key)
        # pipeline needed to
        # avoid race condition on two operations: incr;expire
        # limit on redis
        pipeline = self.client.pipeline()
        pipeline.multi()
        try:
            self.client.incr(formatted_key, 1)
            self.client.expire(formatted_key, self.expire)
            pipeline.execute(raise_on_error=True)
        except RedisError as e:
            raise RedisRateLimitException('{!r}'.format(e))

    def is_limit_exceeded(
            self,
            key: str,
            raise_exception: bool = True,
            bump_counter: bool = True,
    ) -> bool:
        """ Check if limit exceed for key if not bump counter.

        Rate limiter based on example:
            https://redis.io/commands/incr#pattern-rate-limiter-1

        :param key: string_value
        :param raise_exception: if True will raise RateLimitException exception
        :param bump_counter: if limit is not exceed and True will bump counter
        """
        str_key = self._get_key(key)
        current_value = self._get_counter(str_key)
        if current_value and current_value > self.limit:
            if raise_exception:
                raise RedisRateLimitException('Limit exceeded')
            return True
        if bump_counter:
            self._increment_counter(str_key)
        return False

    def get_counter(self, key: str) -> Optional[int]:
        str_key = self._get_key(key)
        return self._get_counter(str_key)

    def increment_counter(self, key: str) -> None:
        str_key = self._get_key(key)
        self._increment_counter(str_key)

    def clear_key(self, key: str):
        return self.client.delete(self._get_key(key))
