import psycopg2

DB_CONFIG = {
    "dbname": "db_coursework",
    "user": "postgres",
    "password": "336314010",
    "host": "localhost",
    "port": "5432",
}

class DatabaseHandler:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)

    def authenticate_user(self, login, hashed_password):
        cursor = self.conn.cursor()
        query = "SELECT user_id, role_id, login, email FROM UserAccount WHERE login = %s AND password = %s"
        cursor.execute(query, (login, hashed_password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return {"user_id": user[0], "role_id": user[1], "login": user[2], "email": user[3]}
        return None

    def register_user(self, login, hashed_password, email):
        cursor = self.conn.cursor()
        try:
            query = """INSERT INTO UserAccount (role_id, login, password, email) VALUES (1, %s, %s, %s)"""
            cursor.execute(query, (login, hashed_password, email))
            self.conn.commit()
            cursor.close()
            return True
        except:
            self.conn.rollback()
            cursor.close()
            return False

    def get_orders_by_user_id(self, user_id):
        # Fetch orders for a specific user ID
        cursor = self.conn.cursor()
        query = """SELECT orders.order_id, jewelrytype.name, useraccount.email, orderstatus.name, total_cost FROM orders
                 JOIN product ON product.product_id = orders.product_id
                 JOIN jewelrytype ON product.jewelry_type_id = jewelrytype.jewelry_type_id
                 JOIN useraccount ON orders.master_id = useraccount.user_id
                 JOIN orderstatus ON orders.status_id = orderstatus.status_id
                 WHERE public.orders.user_id = %s;"""
        cursor.execute(query, str(user_id))
        return cursor.fetchall()

    def update_order_status(self, order_id, status):
        cursor = self.conn.cursor()

        try:
            query = """CALL update_order_status(%s, %s);"""
            cursor.execute(query, (int(order_id), status))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def get_all_products(self):
        cursor = self.conn.cursor()
        query = """SELECT * FROM get_all_products();"""
        cursor.execute(query)
        return cursor.fetchall()

    def update_user_email(self, user_id, email):
        cursor = self.conn.cursor()
        try:
            query = """UPDATE useraccount SET email = %s WHERE user_id = %s"""
            cursor.execute(query, (email, user_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
        return

    def create_order(self, product_id, user_id, type):
        # Fetch orders for a specific user ID
        cursor = self.conn.cursor()
        try:
            query = """SELECT * FROM create_new_order(%s, %s, %s);"""
            cursor.execute(query, (product_id, user_id, type))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
        return

    def get_jewerly_types(self):
        cursor = self.conn.cursor()
        try:
            query = """SELECT jewelry_type_id, name from jewelrytype"""
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()


    def get_metal_types(self):
        cursor = self.conn.cursor()
        try:
            query = """SELECT metal_id, name, cost_gramm from metal"""
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def get_gem_types(self):
        cursor = self.conn.cursor()
        try:
            query = """SELECT jewelry_type_id, name from jewelrytype"""
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()