from cassandra.cluster import Cluster
import uuid

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('ecomm_noopur')

# Define the UPDATE statement
update_query = """
UPDATE shopping_cart SET quantity = ? WHERE user_id = ? AND product_id = ?
"""

# Prepare the UPDATE statement
prepared_update = session.prepare(update_query)

# Execute the UPDATE statement with appropriate values
new_quantity = 50
user_id_value = uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02')
product_id_value = 3
session.execute(prepared_update, (new_quantity, user_id_value, product_id_value))

# Close the Cassandra connection
session.shutdown()
cluster.shutdown()
