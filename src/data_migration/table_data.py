from src.DB_connect.dbconnection import Dbconnect
from datetime import datetime
import pandas as pd

class TableData:
    @staticmethod
    def addStudent(column_data):
        student_name = column_data['student_name']
        srn = column_data['srn']
        class_ = column_data['class']  # Using class_ to avoid conflict with the keyword
        section = column_data['section']
        roll_no = column_data['roll_no']
        phone = column_data['phone']
        address = column_data['address']
        createdOn = datetime.now().strftime('%Y-%m-%d')

        connection = Dbconnect.dbconnects()
        if connection:
            cursor = connection.cursor()
            try:
                query = f"""
                INSERT INTO student (srn, student_name, class, section, roll_no, phone, address, createdOn)
                VALUES ('{srn}', '{student_name}', '{class_}', '{section}', '{roll_no}', '{phone}', '{address}', '{createdOn}')
                """
                cursor.execute(query)
                connection.commit()

                return {'message': 'Student added successfully', 'status': 'success'}
            except Exception as e:
                return {'message': str(e), 'status': 'error'}
            finally:
                cursor.close()  # Always close the cursor
                connection.close()  # Ensure the connection is closed

    @staticmethod
    def addBook(column_data):
        isbn = column_data['isbn']
        title = column_data['title']
        publication = column_data['publication']
        author_name = column_data['author_name']
        price = column_data['price']
        edition = column_data['edition']
        quantity = column_data.get('quantity', 1)  # Default to 1 if not specified
        createdOn = datetime.now().strftime('%Y-%m-%d')

        connection = Dbconnect.dbconnects()
        if connection:
            cursor = connection.cursor()
            try:
                if quantity is None or quantity < 1:
                    return {
                        "message": "Quantity must be at least 1.",
                        "status": "error"
                    }

                for i in range(quantity):
                    query = f"""
                        INSERT INTO book (isbn, title, publication, author_name, price, edition, quantity, createdOn)
                        VALUES ('{isbn}', '{title}', '{publication}', '{author_name}', '{price}', '{edition}', 1, '{createdOn}')
                    """
                    cursor.execute(query)

                connection.commit()

                return {'message': 'Books added successfully', 'status': 'success'}

            except Exception as e:
                return {'message': str(e), 'status': 'error'}

            finally:
                cursor.close()
                connection.close()