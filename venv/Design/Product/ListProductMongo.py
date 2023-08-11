from flask import Flask, jsonify, render_template, send_from_directory
from pymongo import MongoClient
import json

app = Flask(__name__)

# Replace the following with your actual MongoDB connection details
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['ecomm_noopur']
collection = db['item_catalogue']


@app.route('/listProducts')
def list_products():
    try:
        # Retrieve all documents from the collection
        all_documents = list(collection.find())
        print(all_documents)
        # Display all documents
        # print("All records in the collection:")
        # for document in all_documents:
        #     print(document)

        # Conditional filter-- Numeric
        # Replace 'your_database_name' with your desired database name
        # db = mongo_client['ecomm_noopur']
        # Replace 'your_collection_name' with your desired collection name
        # collection = db['item_catalogue']
        # Retrieve documents that match a specific condition (e.g., age greater than 25)
        # query = {"price": {"$gt": 800}}
        # filtered_documents = collection.find(query)
        # Display filtered documents
        # print("Filtered records in the collection:")
        # for document in filtered_documents:
        #    print(document)

        # Conditional filter-- Text
        # Replace 'your_database_name' with your desired database name
        # db = mongo_client['ecomm_noopur']
        # Replace 'your_collection_name' with your desired collection name
        # collection = db['item_catalogue']

        # To enable text search on a specific field, you need to create a text index on that field.
        # Replace 'text_column' with the name of the text field you want to filter on
        # collection.create_index([("item_name", pymongo.TEXT)])
        # Replace 'search_query' with the text you want to search for
        # search_query = "special"
        # query = {"$text": {"$search": search_query}}

        # Find documents that match the text search query
        # search_results = collection.find(query)
        # print("Search results:")
        # for document in search_results:
        #    print(document)

        #return jsonify(all_documents)
        #mongo_client.close()
        return json.dumps(all_documents, default=str, indent=4)



    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define the route to serve images
#@app.route('/images/<path:filename>'
@app.route('/productImages/<path:filename>')
def serve_image(filename):
    return send_from_directory('productImages/', filename)

#@app.route('/listProducts.html')
#def product():
#    return render_template('listProducts.html')

#@app.route('/testImageURL.html')
#def productImage():
#    return render_template('testImageURL.html')

if __name__ == '__main__':
   app.run(debug=True)

#<path:filename>