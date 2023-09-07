from datetime import datetime
import json
import uuid
from cassandra.query import BatchStatement


class ShoppingCart:
    def __init__(self, cluster, session, cassandra_table, cart_data):
        self.cluster = cluster
        self.session = session
        self.cassandra_table = cassandra_table
        self.cart_data = cart_data

    def insert_cart(self, cart_data):
        # Prepare the INSERT statement
        insert_query = f"""
        INSERT INTO {self.cassandra_table} (order_id, added_at, product_id, quantity, user_id)
        VALUES (?, ?, ?, ?, ?)
        """

        prepared_insert = self.session.prepare(insert_query)
        cart_dict = json.loads(cart_data)

        # Generate a new UUID and current timestamp
        user_id = uuid.uuid4()
        order_id = uuid.uuid4()
        current_time = datetime.now()
        data_to_insert = []

        for item in cart_dict:
            if 'id' in item:
                # Insert data into the table
                data_to_insert.append([order_id, current_time, item['id'], item['quantity'], user_id])

        print(data_to_insert)
        batch = BatchStatement()

        # Add each record to the batch
        for record in data_to_insert:
            bound_insert = prepared_insert.bind(record)
            batch.add(bound_insert)

        # Execute the batch statement
        self.session.execute(batch)

        # Close the Cassandra connection
        self.session.shutdown()
        self.cluster.shutdown()

    def delete_from_cart(self):
        # Define the DELETE statement
        delete_query = """
        DELETE FROM shopping_cart WHERE user_id = ? AND product_id = ?
        """

        # Prepare the DELETE statement
        prepared_delete = self.session.prepare(delete_query)

        # Execute the DELETE statement with appropriate values
        user_id_value = self.user_id  # Ruuid.UUID('ddc9919e-2d78-4e52-85dd-04c889069aa5')
        product_id_value = self.product_id
        self.session.execute(prepared_delete, (user_id_value, product_id_value))

        # Close the Cassandra connection
        self.session.shutdown()
        self.cluster.shutdown()

    def update_cart(self):
        # Define the UPDATE statement
        update_query = """
        UPDATE shopping_cart SET quantity = ? WHERE user_id = ? AND product_id = ?
        """

        # Prepare the UPDATE statement
        prepared_update = self.session.prepare(update_query)

        # Execute the UPDATE statement with appropriate values
        new_quantity = self.quantity # 50
        user_id_value = self.user_id # uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02')
        product_id_value = self.product_id # 3
        self.session.execute(prepared_update, (new_quantity, user_id_value, product_id_value))

        # Close the Cassandra connection
        self.session.shutdown()
        self.cluster.shutdown()

    def list_cart(self):
        # Define the SELECT statement
        select_query = """
        SELECT * FROM shopping_cart WHERE user_id = ? AND product_id = ?
        """

        # Prepare the SELECT statement
        prepared_select = self.session.prepare(select_query)

        # Execute the SELECT statement with appropriate values
        user_id_value = self.user_id # uuid.UUID('993012b4-7f57-494f-852f-68673bc5eb02')
        product_id_value = self.product_id
        result_set = self.session.execute(prepared_select, (user_id_value, product_id_value))

        # Process the result set
        for row in result_set:
            print(row)

        # Close the Cassandra connection
        self.session.shutdown()
        self.cluster.shutdown()
