import asyncio
from asyncio import CancelledError


async def say_what(delay, name):
    await asyncio.sleep(delay)
    msg = f'Say what {name}'
    print(msg)
    return msg


async def main():
    tasks = asyncio.all_tasks()
    task1 = asyncio.create_task(say_what(2, 'Dave'))
    task2 = asyncio.create_task(say_what(1, 'Matt'))
    sh_task = asyncio.shield(task1)
    sh_task.cancel()
    await task2
    try:
        await sh_task
    except CancelledError:
        assert not task1.cancelled()
        print(f'Task 1 was not cancelled {not task1.cancelled()}')
    print(f'Result task 2  {task2.result()}')
    # print(f'Result task {sh_task.result()}')
    await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(main(), debug=True)
