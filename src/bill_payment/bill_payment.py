from src.DB_connect.dbconnection import Dbconnect


class Bill_payments:
    @staticmethod
    def save_orders(name,mobile,orders):
        db_connection = Dbconnect()
        connection = db_connection.dbconnects()
        if connection:
            cursor = connection.cursor()
            try:
                order_query = f"INSERT INTO orders (name, mobile) VALUES ('{name}', '{mobile}')"
                cursor.execute(order_query)
                order_id = cursor.lastrowid

                for order_item in orders:
                    sno = sno = order_item["sno"]
                    category = order_item["category"]
                    product = order_item["product"]
                    quantity = order_item["quantity"]
                    products = order_item.get("products", [])
                    order_item_query = f"INSERT INTO order_items (order_id, sno, category, product, quantity, product_id, product_name) VALUES ('{order_id}', '{sno}', '{category}','{product}' ,'{quantity}', '{product_id}', '{product_name}')"
                    cursor.execute(order_item_query)

                    for product in products:
                        product_id = product["product_id"]
                        product_name = product["product_name"]
                        product_query = f"""INSERT INTO order_items(order_id, sno, category, product, quantity, product_id, product_name) VALUES ('{order_id}', '{sno}', '{category}','{product}' ,'{quantity}', '{product_id}', '{product_name}')"""
                        cursor.execute(product_query)
                connection.commit()
                return {"message": "Order saved successfully", "status": "success"}
            except Exception as e:
                connection.rollback()
                return {"error": str(e), "status": "error"}
        else:
            return {"error": "Failed to connect to the database", "status": "error"}








