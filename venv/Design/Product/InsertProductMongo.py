from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import json
import shutil


app = Flask(__name__)

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    global result
    try:
        uploaded_file = request.files['file']

        if uploaded_file:
            # Save the uploaded file to a desired location (e.g., "uploads" folder)
            uploaded_file.save("products/" + uploaded_file.filename)
            # return jsonify({"message": "File upload successful"})

            # MongoDB connection details
            mongo_client = MongoClient('mongodb://localhost:27017/')

            # ***************** Insert bulk data in MONGO DB using JSON file *****************
            db = mongo_client['ecomm_noopur']
            collection = db['item_catalogue']
            source_file_path = 'products/' + uploaded_file.filename
            destination_path = "../uploads/"
            with open(source_file_path, 'r') as json_file:
                data_list = json.load(json_file)
                print(data_list)

            # Ensure data_list is not empty and is a list of dictionaries
            if not data_list or not isinstance(data_list, list):
                print("Error: Invalid or empty data_list.")
            else:
                # Insert bulk data into the collection
                result = collection.insert_many(data_list)

            print(result)
            if result.acknowledged:
                print("Insertion successful.")
                print("Number of documents inserted:", len(result.inserted_ids))
            else:
                print("Insertion failed.")

            mongo_client.close()
            shutil.move(source_file_path, destination_path)
            return jsonify({"success": "File processed"}), 200

        else:
            return jsonify({"error": "No file uploaded"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('insertProduct.html')

if __name__ == '__main__':
    app.run(debug=True)
