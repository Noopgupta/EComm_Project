from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import json
import shutil
import os


class Product:
    def __init__(self, mongo_client, db, collection, product_id):
        self.product_id = product_id
        self.mongo_client = MongoClient(mongo_client)
        self.db = self.mongo_client[db]
        self.collection = self.db[collection]

    # @app.route('/listProducts')
    def list_products(self):
        try:
            # Retrieve all documents from the collection
            all_documents = list(self.collection.find())
            return json.dumps(all_documents, default=str, indent=4)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # @app.route('/insertProduct', methods=['POST'])
    def insert_product(self):
        global result
        try:
            uploaded_file = request.files['file']

            if uploaded_file:
                # Save the uploaded file to a desired location (e.g., "uploads" folder)
                uploaded_file.save("products/" + uploaded_file.filename)

                # ***************** Insert bulk data in MONGO DB using JSON file *****************
                source_file_path = 'products/' + uploaded_file.filename
                destination_path = "../../Project/Design/uploads/"
                with open(source_file_path, 'r') as json_file:
                    data_list = json.load(json_file)
                    print(data_list)

                # Ensure data_list is not empty and is a list of dictionaries
                if not data_list or not isinstance(data_list, list):
                    print("Error: Invalid or empty data_list.")
                else:
                    # Insert bulk data into the collection
                    result = self.collection.insert_many(data_list)

                print(result)
                if result.acknowledged:
                    print("Insertion successful.")
                    print("Number of documents inserted:", len(result.inserted_ids))
                else:
                    print("Insertion failed.")

                self.mongo_client.close()
                # Overwrite the destination file if already exists
                if os.path.exists(destination_path + uploaded_file.filename):
                    os.remove(destination_path + uploaded_file.filename)

                shutil.move(source_file_path, destination_path)
                return jsonify({"success": "File processed"}), 200

            else:
                return jsonify({"error": "No file uploaded"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
