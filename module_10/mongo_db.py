import pymongo
from pymongo.database import Database
from pymongo.collection import Collection
m_uri = "mongodb://mongo_admin:qwe123@localhost:27017/movies_db?retryWrites=true&w=majority"
sw_uri = "mongodb://mongo_admin:qwe123@localhost:27017/sw_db?retryWrites=true&w=majority"

# Write concern https://docs.mongodb.com/manual/reference/write-concern/
movies_mongo_client = pymongo.MongoClient(m_uri)
sw_mongo_client = pymongo.MongoClient(sw_uri)
movies_db: Database = movies_mongo_client.movies_db
sw_db: Database = sw_mongo_client.sw_db
# collection
movies_collection: Collection = movies_db.movies
# sw
sw_films_collection: Collection = sw_db.films
sw_people_collection: Collection = sw_db.people
sw_starships_collection: Collection = sw_db.starships

### JS client
### mongo
### SWITCH TO DATABASE
## use movies_db
## db.movies_db.insert({ _id: 1, name: "Silly MOvie" } })
#  db.movies_db.findOne({_id: 1})
##  delete
# # db.movies_db.deleteOne({_id: 1})
# db.createUser(
# {
#     user: "mongo_admin",
#     pwd: "qwe123",
#     roles: [
#       { role: "readWrite", db: "todo_db" }
#     ]
# })

# db.updateUser(
#     "mongo_admin",
# {
#     roles: [
#       { role: "readWrite", db: "personal_db"},
#         {role: "readWrite", db: "todo_db"}
#     ]
# })
#
#
