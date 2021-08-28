from mongo_db import movies_collection
import pymongo


def get_all():
    movies = movies_collection.find(
        {"year": {"$lte": 2005}}
    ).sort([("year", pymongo.DESCENDING)])
    for movie in movies:
        print(movie)


def get_by_year(year=2005):
    movies = movies_collection.find(
        {"year": {"$lte": year}},
        # with projection
        {"year": 1, "title": 1, "_id": 0}
    ).sort(
        [
            ("year", pymongo.ASCENDING),
            ("title", pymongo.DESCENDING),
        ]
    )
    for movie in movies:
        print(movie)


def get_comedies_with_billy():
    movies = movies_collection.find(
        {
            "$and": [
                {"genres": {"$in": ["Comedy"]}},
                {"cast": {"$elemMatch": {"$regex": "Billy"}}}
            ]
        },
    ).sort([("year", pymongo.ASCENDING)])
    for movie in movies:
        print(movie)


def get_drama_aggregation():
    movies = movies_collection.aggregate(
        [
            {
                "$project": {
                    "title": 1,
                    "cast": 1,
                    "year": 1,
                    "genres": 1,
                    # "number_of_actors": {
                    #     "$cond": {
                    #         "if": {"$isArray": "$genres"},
                    #         "then": {"$size": "$genres"},
                    #         "else": "NA",
                    #     }
                    # }
                }
            },
            {
                "$addFields": {
                    "number_of_actors": {"$size": "$genres"}
                }
            },
            {
                "$match": {"number_of_actors": {"$gte": 3}}
            },
            {
                "$sort": {"number_of_actors": 1, "year": 1},
            }
        ],
    )
    for movie in movies:
        print(movie)


def find_with_js():
    movies = movies_collection.find(
        {
            "$where": """
                function() {
                    // indexOf expensive search operation do not do it in prod
                    return this.title.indexOf('Door') != -1
                };
            """
        },
    )
    for movie in movies:
        print(movie)


if __name__ == '__main__':
    # get_all()
    # get_commedies()
    get_drama_aggregation()
    # find_with_js()
