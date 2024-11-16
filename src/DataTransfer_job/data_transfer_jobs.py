from pickle import STRING
import mysql
import pandas as pd
from flask import jsonify

from src.DB_connect.dbconnection import Dbconnect
import json

from src.data_migration.student import Student
from src.dataframe_df.dataframe_operations import Dataframe_pandas

class DataTransfer:
    @staticmethod
    def create_data_operation(srn,table_name,sql_insert):
        connection = Dbconnect.dbconnects()
        if connection:
            cursor = connection.cursor()
            try:
                create_objects_sql = f"CREATE TABLE {table_name} ({sql_insert})"
                cursor.execute(create_objects_sql)
                message = 'Table created successfully'
            except mysql.connector.Error as error:
                message = f'Error creating table: {error}'
            finally:
                cursor.close()
                connection.close()
            return message
        else:
            return 'Failed to connect to the database'

    @staticmethod
    def save_data_operation(table_name, column_data, action):
        try:
            connection = Dbconnect.dbconnects()
            validation_flag = 0

            if table_name == 'student':
                result = Student.addStudent(column_data)
                return result

            if connection:
                # Extract quantity from column_data if available
                quantity = column_data.get('quantity', 1)  # Default to 1 if not specified
                # Remove quantity from column_data to avoid insertion into the database
                column_data.pop('quantity', None)

                # Prepare a list to hold data for multiple rows
                data_to_insert = []

                # Validate quantity
                if quantity is None or quantity < 1:
                    return {
                        "message": "Quantity must be at least 1.",
                        "status": "error"
                    }

                for i in range(quantity):
                    # Create a copy of the data to insert
                    row_data = column_data.copy()  # Make a copy to avoid overwriting

                    # Set quantity to 1 for each row
                    row_data['quantity'] = 1  # Set quantity to 1 for each row
                    data_to_insert.append(row_data)

                # Normalize the data and create a DataFrame
                data_set = pd.json_normalize(data_to_insert)
                Dataframe_pandas.write_df_to_sql(data_set, table_name, operation='REPLACE')

                if validation_flag == 1:
                    message = 'Fields have an Empty Value'
                    status = "error"
                else:
                    message = 'Books added successfully'
                    status = 'success'

                return {
                    "message": message,
                    "status": status
                }

        except Exception as e:
            return {
                "message": str(e),
                "status": "error",
                "data": ''
            }

    @staticmethod
    def delete_data_operation(table_name, row_id):
        connection = Dbconnect.dbconnects()
        if connection:
            try:
                cursor = connection.cursor()
                # if not isinstance(row_id, int):
                #     return {'status': 'Error', 'message': 'Row ID must be an integer'}

                delete_sql = f"DELETE FROM {table_name} WHERE srn = '{row_id}'"
                cursor.execute(delete_sql)  # Corrected method name
                connection.commit()
                if cursor.rowcount == 0:
                    return {'status': 'Error', 'message': 'No data found to delete'}
                else:
                    return {'status': 'success', 'message': 'Deleted successfully'}
                # return {'status': 'success', 'message': message}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        else:
            return {'status': 'error', 'message': 'Failed to connect to the database'}

    @staticmethod
    def update_data_operation(row_id, column_data, table_name):
        try:
            connection = Dbconnect.dbconnects()
            if not connection:
                return {'status': 'error', 'message': 'Failed to connect to the database'}

            if not column_data:
                return {'status': 'error', 'message': 'No column data provided'}

            set_clause = ', '.join([f"{key} = %s" for key in column_data.keys()])
            update_query = f"UPDATE {table_name} SET {set_clause} WHERE srn = %s"

            cursor = connection.cursor()
            cursor.execute(update_query, list(column_data.values()) + [row_id])
            connection.commit()

            if cursor.rowcount > 0:
                return {'status': 'success', 'message': 'Updated successfully'}
            else:
                return {'status': 'error', 'message': 'No rows were updated'}

        except Exception as e:
            return {'status': 'error', 'message': f"An error occurred: {str(e)}"}
