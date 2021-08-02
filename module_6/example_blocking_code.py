from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from aiomisc import entrypoint
from aiomisc.service import Profiler
import asyncio
import time


async def blocking():
    print('Blocking')
    for i in range(50):
        print(f'Blocking {i}')
        time.sleep(0.1)


async def task2():
    await blocking()


async def task1():
    print('Task 1 star')
    await asyncio.sleep(1.0)
    print('Task 1 stop')


async def main():
    # loop = asyncio.get_event_loop()
    # loop.set_default_executor(ProcessPoolExecutor())
    print('Main start ')
    await asyncio.gather(
        task2(),
        task1()
    )
    print('Main end')

if __name__ == '__main__':
    asyncio.run(main())


