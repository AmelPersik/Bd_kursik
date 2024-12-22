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

    def register_user(self, login, hashed_password, email, role):
        cursor = self.conn.cursor()
        try:
            query = """INSERT INTO UserAccount (role_id, login, password, email) VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (role, login, hashed_password, email))
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
        id = int(user_id)
        query = """SELECT orders.order_id, jewelrytype.name, metal.name, gem.name, useraccount.email, orderstatus.name, total_cost FROM orders
                 JOIN product ON product.product_id = orders.product_id
                 JOIN jewelrytype ON product.jewelry_type_id = jewelrytype.jewelry_type_id
                 JOIN useraccount ON orders.master_id = useraccount.user_id
                 JOIN orderstatus ON orders.status_id = orderstatus.status_id
                 JOIN metal ON product.metal_id = metal.metal_id
                 JOIN gem ON product.gem_id = gem.gem_id
                 WHERE orders.user_id = %s;"""
        cursor.execute(query, (id,))
        return cursor.fetchall()

    def get_orders_by_master_id(self, master_id):
        # Fetch orders for a specific user ID
        cursor = self.conn.cursor()
        query = """SELECT orders.order_id, jewelrytype.name, metal.name, metal.cost_gramm, gem.name, gem.cost_carat, useraccount.email, orderstatus.name, difficulty.coefficient, total_cost FROM orders
                 JOIN product ON product.product_id = orders.product_id
                 JOIN jewelrytype ON product.jewelry_type_id = jewelrytype.jewelry_type_id
                 JOIN useraccount ON orders.master_id = useraccount.user_id
                 JOIN orderstatus ON orders.status_id = orderstatus.status_id
                 JOIN metal ON product.metal_id = metal.metal_id
                 JOIN gem ON product.gem_id = gem.gem_id
                 JOIN difficulty ON product.difficulty_id = difficulty.difficulty_id
                 WHERE public.orders.master_id = %s;"""
        cursor.execute(query, (int(master_id),))
        return cursor.fetchall()

    def get_all_orders(self):
        # Fetch orders for a specific user ID
        cursor = self.conn.cursor()
        query = """SELECT orders.order_id, jewelrytype.name, metal.name, metal.cost_gramm, gem.name, gem.cost_carat, c.email, m.email, orderstatus.name, ordertype.name, difficulty.coefficient, total_cost FROM orders
                    JOIN product ON product.product_id = orders.product_id
                    JOIN jewelrytype ON product.jewelry_type_id = jewelrytype.jewelry_type_id
                    JOIN useraccount m ON orders.master_id = m.user_id
                    JOIN useraccount c ON orders.user_id = c.user_id
                    JOIN orderstatus ON orders.status_id = orderstatus.status_id
                    JOIN metal ON product.metal_id = metal.metal_id
                    JOIN gem ON product.gem_id = gem.gem_id
                    JOIN ordertype ON orders.type_id = ordertype.type_id
                    JOIN difficulty ON product.difficulty_id = difficulty.difficulty_id;"""
        cursor.execute(query)
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

    def create_custom_order(self, _jewelry_type, _selected_metal_id, _metal_weight,
                                             _selected_gem_id, _gem_carat):
        cursor = self.conn.cursor()
        try:
            # Insert the new product with default ID
            query = """INSERT INTO product (jewelry_type_id, metal_id, metal_gramm, gem_id, gem_carat, difficulty_id) 
                               VALUES (%s, %s, %s, %s, %s, %s);"""
            cursor.execute(query, (_jewelry_type, _selected_metal_id, _metal_weight, _selected_gem_id, _gem_carat, 1))

            # Commit the transaction
            self.conn.commit()

            # Retrieve the last inserted ID
            cursor.execute("""select max(product_id) from product;""")
            new_product_id = cursor.fetchone()[0]  # Get the first column of t
            return new_product_id

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
            query = """SELECT gem_id, name, cost_carat from gem"""
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def get_order_difficulties(self):
        cursor = self.conn.cursor()
        try:
            query = """SELECT * from difficulty"""
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def get_order_statuses(self):
        cursor = self.conn.cursor()
        try:
            query = """SELECT * from orderstatus"""
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def update_order_difficulty(self, _current_difficulty, _new_difficulty, _order_id, _difficulty_id):
        cursor = self.conn.cursor()
        _order_id = int(_order_id)
        try:
            query = """UPDATE product
                        SET difficulty_id = %s
                        WHERE product_id = (
                            SELECT product_id
                            FROM orders
                            WHERE order_id = %s
                        );"""
            cursor.execute(query, (_difficulty_id, _order_id))
            query = """UPDATE orders
               SET total_cost = %s / %s * total_cost
               WHERE order_id = %s;"""
            cursor.execute(query, (_new_difficulty, _current_difficulty, _order_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
        return

    def update_order_status(self, _order_id, _status_id):
        cursor = self.conn.cursor()
        _order_id = int(_order_id)
        try:
            query = """UPDATE orders
                        SET status_id = %s
                        WHERE order_id = %s;"""
            cursor.execute(query, (_status_id, _order_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
        return

    def delete_order(self, _order_id):
        cursor = self.conn.cursor()
        try:
            _order_id = int(_order_id)
            query = """DELETE FROM orders WHERE order_id = %s;"""
            cursor.execute(query, (_order_id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
        return