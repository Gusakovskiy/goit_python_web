from tasks import add, hello

if __name__ == '__main__':
    hello()
    # hello.apply_async()
    # to run celery tasks
    add.delay(10, 2)
    # print(result.ready())
