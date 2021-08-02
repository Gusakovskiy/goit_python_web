import asyncio


class AwaitableTimer:
    def __init__(self, coro):
        self.coro = coro

    def __await__(self):
        loop = asyncio.get_event_loop()
        start = loop.time()
        result = yield from self.coro.__await__()
        print('Elapsed {:f}'.format(loop.time() - start))
        return result


async def main():
    print('Timer')
    timer = AwaitableTimer(asyncio.sleep(1.0))
    r = await timer
    print(r)

asyncio.run(main(), debug=True)
