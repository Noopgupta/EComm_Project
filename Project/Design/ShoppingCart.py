from cassandra.cluster import Cluster
# import uuid
from datetime import datetime


class ShoppingCart:
    def __init__(self, cluster, session, user_id, product_id, quantity):
        self.cluster = Cluster(['127.0.0.1'], port=9042)
        self.session = cluster.connect('ecomm_noopur')
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def insert_cart(self):
        # Prepare the INSERT statement
        insert_query = """
        INSERT INTO shopping_cart (user_id, product_id, quantity, added_at)
        VALUES (?, ?, ?, ?)
        """

        prepared_insert = self.session.prepare(insert_query)

        # Generate a new UUID and current timestamp
        # new_uuid = uuid.uuid4()
        current_time = datetime.now()

        # Insert data into the table
        data_to_insert = (self.user_id, self.product_id, self.quantity, current_time)
        self.session.execute(prepared_insert, data_to_insert)

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
