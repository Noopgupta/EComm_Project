import jsonschema
import json

# Define the JSON schema for the expected structure
schema = {
    "type": "object",
    "properties": {
        "item_id": {"type": "integer"},
        "item_name": {"type": "string"},
        "category": {"type": "string"},
        "price": {"type": "integer"},
        "description": {"type": "string"},
        "image_url": {"type": "string", "format": "email"},
        "rating": {"type": "number"},
        "reviews": {"type": "integer"}
    },
    "required": ["item_id", "item_name", "category", "price"]
}

# Sample JSON data to be validated
#json_data = '''
#{
#    "item_id": 6,
#    "item_name": "perform",
#    "category": "school",
#    "price": 228,
#    "description": "Agreement blood collection become laugh write throw.",
#    "image_url": "https://schneider.com/",
#    "rating": 2.2,
#    "reviews": 429
#}
#'''

#try:
#    # Load the JSON data
#    data = json.loads(json_data)
#
#    # Validate the JSON data against the schema
#    jsonschema.validate(data, schema)
#
#    print("JSON data is valid.")
#except jsonschema.exceptions.ValidationError as e:
#    print("JSON data is not valid:", e)


file_path = '/ProjectCode/uploads/ecommerce_data.json'
with open(file_path, 'r') as json_file:
    data_list = json.load(json_file)
    print(len(data_list))

try:
    for i in range(len(data_list)):
    # Validate the JSON data against the schema
        jsonschema.validate(data_list[i], schema)

        print("JSON data is valid.")
except jsonschema.exceptions.ValidationError as e:
    print("JSON data is not valid:", e)
