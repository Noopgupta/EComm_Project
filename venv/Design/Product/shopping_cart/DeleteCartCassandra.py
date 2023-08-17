from cassandra.cluster import Cluster
import uuid

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('ecomm_noopur')

# Define the DELETE statement
delete_query = """
DELETE FROM shopping_cart WHERE user_id = ? AND product_id = ?
"""

# Prepare the DELETE statement
prepared_delete = session.prepare(delete_query)

# Execute the DELETE statement with appropriate values
user_id_value = uuid.UUID('ddc9919e-2d78-4e52-85dd-04c889069aa5')  # Replace with the user ID you want to delete
product_id_value = 2  # Replace with the product ID you want to delete
session.execute(prepared_delete, (user_id_value, product_id_value))

# Close the Cassandra connection
session.shutdown()
cluster.shutdown()