from pymongo import MongoClient

# Replace the following with your actual MongoDB connection details
mongo_client = MongoClient('mongodb://localhost:27017/')


#****************** Code to update bulk data from MONGO DB ******************
db = mongo_client['ecomm_noopur']
collection = db['item_catalogue']
# Update one document that matches the given condition
result = collection.update_one({"item_id": 3}, {"$set": {"category": "Home"}})
# Update all documents that match the given condition
#result = collection.update_many({"rating": {"$gte": 4.5}}, {"$set": {"description": "One of the highest rated product"}})

if result.modified_count > 0:
    print("Update successful.")
    print("Number of documents updated:", result.modified_count)
else:
    print("Update failed. No matching documents found.")



mongo_client.close()


