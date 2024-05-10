import json

from flask import jsonify

from src.DB_connect.dbconnection import Dbconnect
from src.dataframe_df.dataframe_operations import Dataframe_pandas
from datetime import datetime

class GetData:
    @staticmethod
    def getData_common(id, Table_name):
        try:
            # import pdb
            # pdb.set_trace()
            if id:
                sql_query = f"""SELECT * FROM {Table_name} WHERE id = '{id}'"""
            else:
                sql_query = f"""SELECT * FROM {Table_name}"""

            # Pass the id parameter to the read_sql_as_df function
            df = Dataframe_pandas.read_sql_as_df(sql_query)
            if df is not None:
                products_json = json.loads(df.to_json(orient='records'))
                return jsonify({'data': products_json,
                                'message': "Data fetch succesfully",
                                'status': 'success'
                                })
            else:
                return jsonify({'message': 'Failed to fetch data',
                                "status": "error"})
        except Exception as e:
            return {"status": str(e),
                    "message": "failed to fetch Data"}

    @staticmethod
    def searchUser(id, Table_name):
        try:
            # Modify SQL query to use LIKE for partial matching
            sql_query = f"SELECT * FROM {Table_name} WHERE id LIKE '%{id}%' OR Bname LIKE '%{id}%' "
            # Pass the id parameter to the read_sql_as_df function
            df = Dataframe_pandas.read_sql_as_df(sql_query)
            if df is not None:
                # Convert DataFrame to JSON
                products_json = json.loads(df.to_json(orient='records'))
                return jsonify({'data': products_json,
                                'message': "Data fetched successfully",
                                'status': 'success'
                                })
            else:
                return jsonify({'message': 'Failed to fetch user data',
                                "status": "error"})
        except Exception as e:
            return jsonify({"status": "error",
                            "message": str(e)})

    @staticmethod
    def searchBook(title, Table_name):
        try:
            # Modify SQL query to use LIKE for partial matching
            sql_query = f"SELECT * FROM {Table_name} WHERE Title LIKE '%{title}%'"
            # Pass the id parameter to the read_sql_as_df function
            df = Dataframe_pandas.read_sql_as_df(sql_query)
            if df is not None:
                # Convert DataFrame to JSON
                products_json = json.loads(df.to_json(orient='records'))
                return jsonify({'data': products_json,
                                'message': "Data fetched successfully",
                                'status': 'success'
                                })
            else:
                return jsonify({'message': 'Failed to fetch book data',
                                "status": "error"})
        except Exception as e:
            return jsonify({"status": "error",
                            "message": str(e)})


    @staticmethod
    def issue_book(id,Isbn):
        # import pdb
        # pdb.set_trace()
        get_book_details = f"""SELECT * from  book where Isbn ='{Isbn}' And isCheckedOut=0"""
        df = Dataframe_pandas.read_sql_as_df(get_book_details)
        connection = Dbconnect.dbconnects()

        cursor = connection.cursor()
        if df.empty:
            return jsonify({'message': 'There is no book to issue',
                            "status": "error"})
        else:
            book_details = json.loads(df.to_json(orient='records'))
            book_details[0]['Title']
            book_details[0]['Isbn']
            cur_date = datetime.now().strftime("%Y-%m-%d")

            update_book_query = f"""UPDATE book
                                    SET isCheckedOut = 1
                                    WHERE Isbn = '{Isbn}' """
            cursor.execute(update_book_query)
            insert_queue_sql = f"INSERT INTO borrower_book_detail SET Isbn='{Isbn}', Title='{book_details[0]['Title']}',id_card='{id}', issued_at='{cur_date}', end_date = '{cur_date}'"
            cursor.execute(insert_queue_sql)
            connection.commit()
            return jsonify({
                            'message': f"Book {book_details[0]['Title']} issued successfully",
                            'status': 'success'
                            })

    @staticmethod
    def allUserBook(id,Isbn):
        # import pdb
        # pdb.set_trace()
        if Isbn == '0':
            get_all_book = f"SELECT * from  borrower_book_detail WHERE id_card ='{id}'"
        else:
            get_all_book = f"SELECT * from  borrower_book_detail WHERE id_card ='{id}' AND Isbn= '{Isbn}'"
        df = Dataframe_pandas.read_sql_as_df(get_all_book)
        if df.empty:
            return jsonify({'message': 'There is no book issued to this user',
                            "status": "error"})
        else:
            all_books = json.loads(df.to_json(orient='records'))
            # Convert timestamps to readable date format
            for book in all_books:
                book['end_date'] = datetime.fromtimestamp(book['end_date'] / 1000).strftime('%Y-%m-%d')
                book['issued_at'] = datetime.fromtimestamp(book['issued_at'] / 1000).strftime('%Y-%m-%d')

            return jsonify({'data': all_books,
                            'message': "Data fetch succesfully",
                            'status': 'success'
                            })

    @staticmethod
    def calculate_fine(id, Isbn):
        get_fine = f"SELECT * from  borrower_book_detail WHERE id_card ='{id}' AND Isbn= '{Isbn}'"
        df = Dataframe_pandas.read_sql_as_df(get_fine)
        connection = Dbconnect.dbconnects()
        cursor= connection.cursor()
        if df.empty:
            return jsonify({'message': 'There is no book issued to this user',
                            "status": "error"})
        else:
            cur_date_str = datetime.now().strftime("%Y-%m-%d")
            book_detail = json.loads(df.to_json(orient='records'))
            end_date_str = datetime.fromtimestamp(book_detail[0]['end_date'] / 1000).strftime('%Y-%m-%d')

            cur_date = datetime.strptime(cur_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            if cur_date <= end_date:
                jsonify({
                    "data": {
                        "calculate_fine": 0
                    },
                    "message": "There is no fine",
                    "status": "success"
                })
            else:
                difference_in_days = (cur_date - end_date).days
                calculate_fine = int(difference_in_days) * 10
                update_fine = f"""UPDATE borrower_book_detail SET fine = '{calculate_fine}' where Isbn='{Isbn}'"""
                cursor.execute(update_fine)
                connection.commit()
                return jsonify({
                                "data": {
                                        "calculate_fine": calculate_fine,
                                        "late_days": difference_in_days
                                        },
                                "message": "Fine has been calculated",
                                "status": "success"
                                 })

    @staticmethod
    def submit_fine(id, Isbn):
        connection = Dbconnect.dbconnects()
        cursor = connection.cursor()
        default_fine = 0
        update_fine = f"""UPDATE borrower_book_detail SET fine = '{default_fine}' where Isbn='{Isbn}' AND id_card='{id}'"""
        cursor.execute(update_fine)
        connection.commit()
        return jsonify({
            "status":"success",
            "message":"fine has been submitted successfully"
        })
    @staticmethod
    def get_saved_order():
        connection = Dbconnect.dbconnects()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT 
                        o.name, o.mobile,
                        oi.sno, oi.category_id, oi.product_id, oi.quantity, oi.category_name, oi.product_name
                    FROM 
                        Orders o
                    JOIN 
                        OrderDetails oi ON o.order_id = oi.order_id
                """)
                saved_orders = cursor.fetchall()

                # Initialize variables to store name, mobile, and orders
                name = None
                mobile = None
                orders = []

                # Iterate over the saved_orders to extract name, mobile, and orders
                for order in saved_orders:
                    name = order['name']
                    mobile = order['mobile']
                    orders.append({
                        "sno": order['sno'],
                        "category_id": order['category_id'],
                        "product_id": order['product_id'],
                        "quantity": order['quantity'],
                        "category_name": order['category_name'],
                        "product_name": order['product_name']
                    })

                # Construct the response dictionary
                response = {
                    "name": name,
                    "mobile": mobile,
                    "orders": orders,
                                    }

                return {"data":response,
                        "message":"Data fetch successfully",
                        "status":"success"}
            except Exception as e:
                return {"error": str(e), "status": "error"}
            finally:
                cursor.close()
                connection.close()
        else:
            return {"error": "Failed to connect to the database", "status": "error"}