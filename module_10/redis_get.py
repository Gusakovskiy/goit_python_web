import time

from module_10.redis_client import client


def set_value():
    sleep = 3.0
    value = client.set('foo', 'bar', ex=3)
    print("After set", value)
    print("Get", client.get('foo'))
    time.sleep(sleep)
    print(f'{sleep} second later', client.get('foo'))


if __name__ == '__main__':
    # Redis commands references:
    # https://redis.io/commands
    set_value()