from flask import jsonify
from pymongo import MongoClient


class Order:
    def __init__(self, mongo_client, db, collection, cart_data):
        self.cart_data = cart_data
        self.mongo_client = MongoClient(mongo_client)
        self.db = self.mongo_client[db]
        self.collection = self.db[collection]

    def insert_order(self, cart_data):

        try:
            print(cart_data)
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

            print(products_to_insert)

            order_id = cart_data[i][0]
            user_id = cart_data[i][1]
            order_date = cart_data[i][2].strftime('%Y-%m-%dT%H:%M:%SZ')

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

            print(user_data)

            # Insert the data into the collection

            result = self.collection.insert_one(user_data)
            print(result)
            if result.acknowledged:
                print("Insertion successful.")
            else:
                print("Insertion failed.")

            # Close the MongoDB connection
            self.mongo_client.close()

        except Exception as e:
            return jsonify({"error": str(e)}), 500

