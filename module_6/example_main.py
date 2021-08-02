import asyncio


async def main():
    print('HI')
    await asyncio.sleep(1)
    print('Guys')


if __name__ == '__main__':
    asyncio.run(main())
