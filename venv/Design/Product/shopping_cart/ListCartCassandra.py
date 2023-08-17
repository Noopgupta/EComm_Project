from cassandra.cluster import Cluster
import uuid

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('ecomm_noopur')

# Define the SELECT statement
select_query = """
SELECT * FROM shopping_cart WHERE user_id = ? AND product_id = ?
"""

# Prepare the SELECT statement
prepared_select = session.prepare(select_query)

# Execute the SELECT statement with appropriate values
user_id_value = uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02')
product_id_value = 3
result_set = session.execute(prepared_select, (user_id_value, product_id_value))

# Process the result set
for row in result_set:
    print(row)

# Close the Cassandra connection
session.shutdown()
cluster.shutdown()
