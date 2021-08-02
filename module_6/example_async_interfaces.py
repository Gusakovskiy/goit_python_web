import asyncio
import aiohttp


class StarWarsPlanetIterator:  # async iterator

    def __init__(self, limit):
        self._base_url = 'https://swapi.dev/api/planets/{}/'
        self.limit = limit + 1
        self.counter = 1
        self.headers = {
            'Accept': 'application/json',
        }

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.counter >= self.limit:
            raise StopAsyncIteration
        async with aiohttp.ClientSession() as session: # async context manager
            async with session.get(
                    self._base_url.format(self.counter), verify_ssl=False, headers=self.headers
            ) as response:
                print("Status:", response.status)
                planet = await response.json()
                self.counter += 1
                return planet


async def star_wars_person_generator(limit):  # async generator
    """Yield numbers from 0 to `to` every `delay` seconds."""
    _base_url = 'http://swapi.dev/api/people/{}/'
    headers = {
        'Accept': 'application/json',
    }
    async with aiohttp.ClientSession() as session:  # async context manager
        for _id in range(1, limit + 1):
            async with session.get(_base_url.format(_id), verify_ssl=False, headers=headers) as response:
                print("Status:", response.status)
                planet = await response.json()
                yield planet


async def main():
    it = StarWarsPlanetIterator(5)
    async for planet in it:
        print(planet)
    # async for person in star_wars_person_generator(3):
    #     print(person['name'])
    #     print(person['eye_color'])
    #     print(person['birth_year'])
    #     print('')


if __name__ == '__main__':
    asyncio.run(main())
