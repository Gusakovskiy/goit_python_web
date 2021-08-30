import requests
from urllib import parse
from mongo_db import sw_db, sw_films_collection, sw_people_collection, sw_starships_collection
base_url = 'https://swapi.dev/api/'

s = requests.Session()


def _insert_value(till, template, collection, _from=1):
    for _id in range(_from, till):
        object_url = template.format(_id)
        url = parse.urljoin(base_url, object_url)
        response = s.get(url)
        if response.status_code == 404:
            # ignore
            continue
        response.raise_for_status()
        print(f'Inserted {object_url}')
        doc = response.json()
        print(doc)
        collection.insert_one(response.json())


def create_films():
    _insert_value(7, 'films/{}/', sw_films_collection)


def create_people():
    _insert_value(
        till=100, _from=1,
        template='people/{}/',
        collection=sw_people_collection,
    )


def create_starships():
    _insert_value(10, 'starships/{}/', sw_starships_collection)


def main():
    create_films()
    create_people()
    create_starships()


if __name__ == "__main__":
    # not needed because already created
    # sw_db.create_collection("films")
    # sw_db.create_collection("people")
    # sw_db.create_collection("starships")
    # main()
    sw_people_collection.create_index(
        [
            ("name", "text"),
            ("hair_color", "text"),
            ("eye_color", "text"),
        ]
    )