from pymongo import MongoClient
from Logger import Logger
import json


config_path = '/home/noopur/IdeaProjects/EComm_Noopur/Project/Design/resources/config.json'

# Load configuration from JSON file
with open(config_path) as config_file:
    config = json.load(config_file)
order_log_file = config["logger"]["order_log_file"]
order_logger = Logger(order_log_file, 'ord')

class Order:
    def __init__(self, mongo_client, db, collection, cart_data):
        self.cart_data = cart_data
        self.mongo_client = MongoClient(mongo_client)
        self.db = self.mongo_client[db]
        self.collection = self.db[collection]

    def insert_order(self, cart_data):

        try:
            products_to_insert = []
            for i in range(len(cart_data)):
                products_to_insert.append([
                    {
                        "product_id": cart_data[i][3],
                        "product_name": cart_data[i][5],
                        "quantity": cart_data[i][4],
                        "price": cart_data[i][6]
                    }
                ])

            order_id = cart_data[0][0]
            user_id = cart_data[0][1]
            order_date = cart_data[0][2].strftime('%Y-%m-%dT%H:%M:%SZ')

            user_data = {
                "_id": user_id,
                "username": "john_doe",
                "email": "john@example.com",
                "password": "hashed_password",
                "full_name": "John Doe",
                "address": "123 Main St",
                "phone_number": "+1234567890",
                "orders": [
                    {
                        "order_id": order_id,
                        "order_date": order_date,
                        "products": products_to_insert
                    }
                ]
            }

            # Insert the data into the collection

            result = self.collection.insert_one(user_data)
            if result.acknowledged:
                print("Insertion successful.")
            else:
                print("Insertion failed.")

            # Close the MongoDB connection
            self.mongo_client.close()

        except Exception as e:
            # Log the error
            order_logger.log_error(str(e))
        else:
            # Log a success message
            order_logger.log_message(user_data)

