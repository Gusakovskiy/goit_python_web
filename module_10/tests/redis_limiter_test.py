import pytest

from module_10.redis_limiter import RedisRateLimiter, RedisRateLimitException

_USER_IP = '127.0.0.12'
_USER_EMAIL = 'fake.user@example.com'


@pytest.mark.parametrize('limit, interval, num_calls', [
    (4, 10, 3),  # 3 calls in 10 seconds with limit 4 calls in 10 seconds
    (110, 1, 101),  # 101 call  in 1 second with limit 101
    (5, 100, 5),  # 5 calls with limit 100 second
])
def test_redis_limiter_no_limit(limit, interval, num_calls):
    prefix = 'test_rate_limiter_ip'
    key = _USER_IP
    limiter = RedisRateLimiter(limit, interval, prefix)
    for _ in range(num_calls):
        limiter.increment_counter(key)
    value = limiter.get_counter(key)
    assert value == num_calls
    assert limiter.is_limit_exceeded(key) is False
    # clear key
    limiter.clear_key(key)


@pytest.mark.parametrize('limit, interval, num_calls, exceed', [
    (3, 1, 4, True),
    (5, 10, 4, False),
    (8, 10, 4, False),
])
def test_is_limit_exceeded(limit, interval, num_calls, exceed):
    prefix = 'test_rate_limiter_email'
    key = _USER_EMAIL
    limiter = RedisRateLimiter(limit, interval, prefix)
    counter = 0
    for _ in range(num_calls):
        limiter.is_limit_exceeded(key, raise_exception=False)
        counter += 1

    assert limiter.is_limit_exceeded(key, raise_exception=False) is exceed
    counter += 1
    if (counter + 1) == limit:
        with pytest.raises(RedisRateLimitException):
            limiter.is_limit_exceeded(key, raise_exception=True)
    # clear key
    limiter.clear_key(key)
