import asyncio
from asyncio import CancelledError


async def say_what(delay, name):
    await asyncio.sleep(delay)
    msg = f'Say what {name}'
    print(msg)
    return msg


async def main():
    task1 = asyncio.create_task(say_what(2, 'Dave'))
    task2 = asyncio.create_task(say_what(1, 'Matt'))
    task1.cancel()
    await task2
    try:
        await task1
    except CancelledError:
        assert not task1.cancelled()
        print(f'Task 1 was cancelled {not task1.cancelled()}')
    print(f'Result task2  {task2.result()}')
    await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main(), debug=True)
