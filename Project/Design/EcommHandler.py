from OrderHandling import Order
from ProductHandling import Product
from ShoppingCart import ShoppingCart
from Logger import Logger
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from cassandra.cluster import Cluster
import uuid
from confluent_kafka import Producer


kafka_config = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka broker(s) address
    'client.id': 'python-producer'
}

producer = Producer(kafka_config)


config_path = '/home/noopur/IdeaProjects/EComm_Noopur/Project/Design/resources/config.json'

# Load configuration from JSON file
with open(config_path) as config_file:
    config = json.load(config_file)

# Kafka detail
topic_name = config["kafka"]["topic_name"]

# MongoDB's connection details
mongodb_host = config["mongodb"]["host"]
mongodb_database = config["mongodb"]["database"]
mongodb_user_collection = config["mongodb"]["user_collection"]
mongodb_product_collection = config["mongodb"]["product_collection"]

# Cassandra's connection details
cassandra_host = config["cassandra"]["host"]
cassandra_port = config["cassandra"]["port"]
cassandra_keyspace = config["cassandra"]["keyspace"]
cassandra_table = config["cassandra"]["table"]
cassandra_cluster = Cluster([cassandra_host], port=cassandra_port)
cassandra_session = cassandra_cluster.connect(cassandra_keyspace)

# Logger details
product_log_file = config["logger"]["product_log_file"]
shopping_cart_log_file = config["logger"]["shopping_cart_log_file"]
order_log_file = config["logger"]["order_log_file"]

sc_logger = Logger(shopping_cart_log_file, 'sc')
product_logger = Logger(product_log_file, 'prd')
order_logger = Logger(order_log_file, 'ord')

app = Flask(__name__)
CORS(app)


class EcommHandler:
    def __init__(self):
        pass


@app.route('/listProducts')
def list_products():
    try:
        product = Product(mongodb_host, mongodb_database, mongodb_product_collection, 1)
    except Exception as e:
        # Log the error
        product_logger.log_error(str(e))
    else:
        # Log a success message
        product_logger.log_message(data=None)
        return product.list_products()


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    try:
        product = Product(mongodb_host, mongodb_database, mongodb_product_collection, 1)
    except Exception as e:
        # Log the error
        product_logger.log_error(str(e))
    else:
        # Log a success message
        product_logger.log_message(data=None)
        return product.insert_product()


@app.route('/')
def index():
    return render_template('insertProduct.html')


@app.route('/cart', methods=['POST'])
def receive_cart_data():
    try:
        cart_data = request.json  # JSON data sent in the request body
        cart_details = insert_cart(cart_data)
        # Create a dictionary for log data as a combination of cart and headers data
        # log_data = {"data": cart_data, "headers": request.headers}
        # log_data = json.dumps(log_data)
        insert_order(cart_details)  # Call it at checkout only ****************
    except Exception as e:
        # Log the error
        sc_logger.log_error(str(e))
    else:
        # Log a success message
        sc_logger.log_message(cart_data)
        send_log_to_kafka(cart_data, topic_name)
        return jsonify({'message': cart_data})


def insert_order(cart_data):
    try:
        order = Order(mongodb_host, mongodb_database, mongodb_user_collection, cart_data)
    except Exception as e:
        # Log the error
        order_logger.log_error(str(e))
    else:
        # Log a success message
        order_logger.log_message(cart_data)
        return order.insert_order(cart_data)


def insert_cart(cart_data):
    try:
        sc = ShoppingCart(cassandra_cluster, cassandra_session, cassandra_table)
    except Exception as e:
        # Log the error
        sc_logger.log_error(str(e))
    else:
        # Log a success message
        sc_logger.log_message(cart_data)
        return sc.insert_cart(cart_data)


def delete_from_cart():
    sc = ShoppingCart(cassandra_cluster, cassandra_session, uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02'), 3, 40)
    return sc.delete_from_cart()


def update_cart():
    sc = ShoppingCart(cassandra_cluster, cassandra_session, uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02'), 3, 40)
    return sc.update_cart()


def list_cart():
    sc = ShoppingCart(cassandra_cluster, cassandra_session, uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02'), 3, 40)
    return sc.list_cart()


def send_log_to_kafka(log_message, topic_name):
    producer.produce(topic=topic_name, value=log_message)
    producer.flush()


if __name__ == '__main__':
    app.run(debug=True)
