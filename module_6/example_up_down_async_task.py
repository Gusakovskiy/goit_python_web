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
    tasks1 = asyncio.create_task(count_up(10))
    tasks2 = asyncio.create_task(count_down(10))
    await tasks1
    await tasks2
    print('Done')

if __name__ == '__main__':
    asyncio.run(main())
