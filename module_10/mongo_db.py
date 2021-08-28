import pymongo
from pymongo.database import Database
from pymongo.collection import Collection
_uri = "mongodb://mongo_admin:qwe123@localhost:27017/movies_db?retryWrites=true&w=majority"
# Write concern https://docs.mongodb.com/manual/reference/write-concern/
mongo_client = pymongo.MongoClient(_uri)
movies_db: Database = mongo_client.movies_db
movies_collection: Collection = movies_db.movies
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
#       { role: "readWrite", db: "movies_db" }
#     ]
# })
#
#
