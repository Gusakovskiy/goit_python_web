from mongo_db import sw_db, sw_films_collection, sw_people_collection, sw_starships_collection

_FIELDS = {"name": 1, "hair_color": 1, "eye_color": 1}


def all_people():
    people = sw_people_collection.find(
        dict(),
        dict(name=1, url=1, hair_color=1, films=1)
    )
    for person in people:
        print(person)


def find_people(query):
    people = sw_people_collection.find(
        {
            "$text": {
                "$search": query,
                "$language": "english",
                 "$caseSensitive": False,
            }
        },
        _FIELDS
    )
    print(f"Query {query}")
    for person in people:
        print(person)
    print(" ")


def films_info():
    _fields = {
        "name": 1,
        "url": 1,
        # "films": 1,
        "joined_films": 1,
    }
    query = sw_people_collection.find(
        dict(),
        _fields
    )
    people = sw_people_collection.aggregate([
        {
            "$lookup":  {
                "from": "films",
                "localField": "films",
                "foreignField": "url",
                "as": "joined_films",
                "pipeline": [
                    {
                        "$project": {
                            "title": 1,
                            "director": 1,
                            "r_date": {
                                "$dateFromString": {
                                    "dateString": "$release_date",
                                    "format": "%Y-%m-%d",
                                }
                            },
                        }
                    },
                ]
            }
        },
        {"$project": _fields},
    ])
    for person in people:
        print('')
        for field in _fields:
            if field == 'joined_films' or field == 'joined_starships':
                continue
            print(f'{field} {person[field]}')
        for film in person['joined_films']:
            print(film)


if __name__ == '__main__':
    # all_people()
    # find_people(query="Luke")
    # find_people(query="R2 D2")
    # find_people(query="Darth")
    # find_people(query="Dar")
    # find_people(query="brown")
    # find_people(query="blu")
    films_info()