import asyncio


async def async_range_down(count):
    while count > 0:
        yield count
        count -= 1
        await asyncio.sleep(1)


async def async_range_up(count):
    counter = 0
    while counter < count:
        yield counter
        counter += 1
        await asyncio.sleep(1)


async def count_up(count):
    async for _id in async_range_up(count):
        print("Up ", _id)


async def count_down(count):
    async for _id in async_range_down(count):
        print("Down ", _id)


async def main():
    print('Start')
    future_1 = asyncio.ensure_future(count_up(10))
    future_2 = asyncio.ensure_future(count_down(10))
    await future_1
    await future_2
    if future_1.done():
        print(future_1.result())
    if future_2.done():
        print(future_2.result())
    print('Done')

if __name__ == '__main__':
    # more about difference in tasks and corutines
    # https://ru.stackoverflow.com/questions/902586/asyncio-%D0%9E%D1%82%D0%BB%D0%B8%D1%87%D0%B8%D0%B5-tasks-%D0%BE%D1%82-future
    asyncio.run(main())
