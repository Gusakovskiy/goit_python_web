import asyncio
import time

async def count_up(count):
    counter = 0
    while counter < count:
        print("Up", counter)
        counter += 1
        time.sleep(1)


async def count_down(count):
    while count > 0:
        print("Down ", count)
        time.sleep(1)
        count -= 1


async def main():
    tasks1 = asyncio.create_task(count_up(10))
    tasks2 = asyncio.create_task(count_down(10))
    await tasks1
    await tasks2
    print(f'Result task {tasks1.result()}')
    print(f'Result task {tasks2.result()}')


if __name__ == '__main__':
    asyncio.run(main())
