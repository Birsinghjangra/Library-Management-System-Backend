from src.DB_connect.dbconnection import Dbconnect
from datetime import datetime


class Student:
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
                # Inserting the new student into the database
                query1 = f"""
                INSERT INTO student (srn, student_name, class, section, roll_no, phone, address, createdOn)
                VALUES ('{srn}', '{student_name}', '{class_}', '{section}', '{roll_no}', '{phone}', '{address}', '{createdOn}')
                """
                print(query1)  # For debugging purposes
                cursor.execute(query1)
                connection.commit()

                return {'message': 'Student added successfully', 'status': 'success'}
            except Exception as e:
                return {'message': str(e), 'status': 'error'}
            finally:
                cursor.close()  # Always close the cursor
                connection.close()  # Ensure the connection is closed