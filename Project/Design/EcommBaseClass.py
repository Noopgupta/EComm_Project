from ProductHandling import Product
from ShoppingCart import ShoppingCart
import json
from flask import Flask, render_template
from flask_cors import CORS
from cassandra.cluster import Cluster
import uuid

config_path = '/home/noopur/IdeaProjects/EComm_Noopur/Project/Design/resources/config.json'

# Load configuration from JSON file
with open(config_path) as config_file:
    config = json.load(config_file)

# MongoDB's connection details
mongodb_host = config["mongodb"]["host"]
mongodb_database = config["mongodb"]["database"]
mongodb_collection = config["mongodb"]["collection"]

# Cassandra's connection details
cassandra_host = config["cassandra"]["host"]
cassandra_port = config["cassandra"]["port"]
cassandra_keyspace = config["cassandra"]["keyspace"]
cassandra_table = config["cassandra"]["table"]
cassandra_cluster = Cluster([cassandra_host], port=cassandra_port)
cassandra_session = cassandra_cluster.connect(cassandra_keyspace)

app = Flask(__name__)
CORS(app)


class EcommBaseClass:
    def __init__(self):
        pass


@app.route('/listProducts')
def list_products():
    product = Product(mongodb_host, mongodb_database, mongodb_collection, 1)
    return product.list_products()


@app.route('/insertProduct', methods=['POST'])
def insert_product():
    product = Product(mongodb_host, mongodb_database, mongodb_collection, 1)
    return product.insert_product()


@app.route('/')
def index():
    return render_template('insertProduct.html')


def insert_cart():
    sc = ShoppingCart(cassandra_cluster, cassandra_session, uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02'), 3, 40)
    return sc.insert_cart()


def delete_from_cart():
    sc = ShoppingCart(cassandra_cluster, cassandra_session, uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02'), 3, 40)
    return sc.delete_from_cart()


def update_cart():
    sc = ShoppingCart(cassandra_cluster, cassandra_session, uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02'), 3, 40)
    return sc.update_cart()


def list_cart():
    sc = ShoppingCart(cassandra_cluster, cassandra_session, uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02'), 3, 40)
    return sc.list_cart()


if __name__ == '__main__':
    app.run(debug=True)
