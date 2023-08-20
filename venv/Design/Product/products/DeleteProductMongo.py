from pymongo import MongoClient
from bson import ObjectId

# Replace the following with your actual MongoDB connection details
mongo_client = MongoClient('mongodb://localhost:27017/')

# ****************** Code to delete data from MONGO DB ******************
db = mongo_client['ecomm_noopur']
collection = db['item_catalogue']
# Delete one document that matches the given condition
#result = collection.delete_one({"item_id": 1})
# Delete all documents that match the given condition
# result = collection.delete_many({"item_id": {"$gte": 5}})

string_ids = ["64d10b358f859266a83f4ecf", "64d10b358f859266a83f4ecd", "64d10b358f859266a83f4ecc"]

# Convert string IDs to ObjectId objects
object_ids = [ObjectId(id) for id in string_ids]
result = collection.delete_many({ "_id": {"$nin": object_ids}})

if result.deleted_count > 0:
    print("Deletion successful.")
    print("Number of documents deleted:", result.deleted_count)
else:
    print("Deletion failed. No matching documents found.")

mongo_client.close()

