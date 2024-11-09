import json

from flask import jsonify, request

from src.DB_connect.dbconnection import Dbconnect
from src.dataframe_df.dataframe_operations import Dataframe_pandas
from datetime import datetime, timedelta


class GetData:
    @staticmethod
    def getData_common(srn, Table_name):
        try:
            # import pdb
            # pdb.set_trace()
            if srn:
                sql_query = f"""SELECT * FROM {Table_name} WHERE srn = '{srn}'"""
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
    def searchUser(srn, Table_name):
        try:
            # Modify SQL query to use LIKE for partial matching
            sql_query = f"""
            SELECT * FROM {Table_name} 
            WHERE srn LIKE '%{srn}%' 
            OR student_name LIKE '%{srn}%'
            """
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
    def searchBook(title,isbn, Table_name):
        try:
            # Modify SQL query to use LIKE for partial matching
            # if isbn != '':
            #     sql_query = f"SELECT Title,isbn FROM {Table_name} WHERE isbn={isbn }AND isCheckedOut = 0"
            # else:
            sql_query = f"SELECT DISTINCT isbn, title, price FROM {Table_name} WHERE title LIKE '%{title}%' AND isCheckedOut = 0"
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
    def issue_book(srn, isbn):
        try:
            connection = Dbconnect.dbconnects()
            cursor = connection.cursor()

            # Check if the book is available for issuing
            query = f"SELECT b.book_id, b.isbn, b.title, b.author_name, b.publication, s.srn, s.student_name, s.class, s.roll_no FROM book AS b LEFT JOIN student AS s ON s.srn = b.srn where b.isbn={isbn} AND b.isCheckedOut = 0"
            book_details= Dataframe_pandas.read_sql_as_df(query)

            if book_details.empty:
                return jsonify({'message': 'The book is not available for issuing', 'status': 'error'})
            else:
                book_id = book_details.iloc[0]['book_id']
                isbn = book_details.iloc[0]['isbn']
                title = book_details.iloc[0]['title']
                author_name = book_details.iloc[0]['author_name']

                student_name = request.json.get('student_name')
                issue_date = datetime.now().strftime("%Y-%m-%d")
                return_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                remark = request.json.get('remark', '')

            # Update book status to checked out
            update_book_query = f"UPDATE book SET isCheckedOut = 1 WHERE book_id = '{book_id}'"
            cursor.execute(update_book_query)

            insert_issue_query = f"""
                INSERT INTO borrower_book_detail (srn, student_name, class, section, book_id, isbn, title, author_name, issued_at, end_date, remark)
                VALUES ('{srn}', '{student_name}', '{request.json.get('class')}', '{request.json.get('section')}',
                        '{book_id}', '{isbn}', '{title}', '{author_name}', '{issue_date}', '{return_date}', '{remark}')
            """
            cursor.execute(insert_issue_query)
            connection.commit()

            return jsonify({'message': f"Book '{title}' issued successfully", 'status': 'success'})
        except Exception as e:
            return jsonify({"status": "error",
                            "message": str(e)})

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
    def calculate_fine(id, isb):
        get_fine = f"SELECT * from  borrower_book_detail WHERE id_card ='{id}' AND isbn= '{isbn}'"
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
                update_fine = f"""UPDATE borrower_book_detail SET fine = '{calculate_fine}' where isbn='{isbn}'"""
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
    def submit_fine(id, isbn):
        connection = Dbconnect.dbconnects()
        cursor = connection.cursor()
        default_fine = 0
        update_fine = f"""UPDATE borrower_book_detail SET fine = '{default_fine}' where isbn='{isbn}' AND id_card='{id}'"""
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