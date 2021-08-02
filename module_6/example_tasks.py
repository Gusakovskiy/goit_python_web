import asyncio


async def say_what(delay, name):
    await asyncio.sleep(delay)
    return f'Say what {name}'


async def main():
    print(asyncio.all_tasks())
    tasks1 = asyncio.create_task(say_what(2, 'Dave'))
    tasks2 = asyncio.create_task(say_what(1, 'Matt'))
    await tasks1
    await tasks2
    print(f'Result task {tasks1.result()}')
    print(f'Result task {tasks2.result()}')

if __name__ == '__main__':
    asyncio.run(main())
