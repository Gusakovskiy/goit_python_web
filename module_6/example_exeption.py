import asyncio


class MyException(Exception):
    ...


async def error():
    raise MyException('ERROR')


async def main():
    # task = asyncio.create_task(error())
    await error()
    # print(task.result())


if __name__ == '__main__':
    # https://docs.python.org/3.6/library/asyncio-dev.html?highlight=exception#detect-exceptions-never-consumed
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main())
    loop.run_forever()
    loop.close()