from mongo_db import movies_collection

import requests


def main():
    response = requests.get(
            'https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json',
            timeout=3.0
    )
    response.raise_for_status()
    movies_response = response.json()
    print(f"GOT movies {len(movies_response)}")
    # for movie in movies:
    result = movies_collection.insert_many(movies_response)
    print(f"Result insertion mongo_db {result}")


if __name__ == '__main__':
    main()
