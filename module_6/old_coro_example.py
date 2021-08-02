import asyncio


@asyncio.coroutine
def old_coro():
    print('Hello')
    yield from asyncio.sleep(1)
    print('world')


def generator():
    print('How you ')
    name = yield 1
    yield 2
    print('doing {}'.format(name))
    yield 3


def main():
    loop = asyncio.get_event_loop()
    coro = old_coro()
    loop.run_until_complete(coro)
    # g = generator()
    # v = next(g)
    # g.send('Jessica')
    # print('Main value '.format(v))
    # next(g)



m = main()