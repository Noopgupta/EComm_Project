from cassandra.cluster import Cluster
import uuid
from datetime import datetime

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('ecomm_noopur')

# Prepare the INSERT statement
insert_query = """
INSERT INTO shopping_cart (user_id, product_id, quantity, added_at)
VALUES (?, ?, ?, ?)
"""

prepared_insert = session.prepare(insert_query)

# Generate a new UUID and current timestamp
new_uuid = uuid.uuid4()
current_time = datetime.now()

# Insert data into the table
data_to_insert = (new_uuid, 4, 6, current_time)
session.execute(prepared_insert, data_to_insert)

# Close the Cassandra connection
session.shutdown()
cluster.shutdown()