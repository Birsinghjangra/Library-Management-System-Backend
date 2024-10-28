from pickle import STRING

import mysql
import pandas as pd
from flask import jsonify

from src.DB_connect.dbconnection import Dbconnect
import json

from src.data_migration.borrower import Borrower
from src.dataframe_df.dataframe_operations import Dataframe_pandas


class DataTransfer:
    @staticmethod
    def create_data_operation(id,table_name,sql_insert):
        message = ''
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
            # print("line 38",table_name)
            # print("line 39", column_data)

            connection = Dbconnect.dbconnects()
            validation_flag = 0
            if table_name == 'borrower':
                result = Borrower.addborower(column_data)
                return result


            if connection:
                column_data_json =column_data
                data_set = pd.json_normalize(column_data_json)
                Dataframe_pandas.write_df_to_sql(data_set, table_name, operation='REPLACE')
            if validation_flag == 1:
                message = 'Fields has an Empty Value',
                status = "error"
            else:
                message = 'Book added successfully'
                status = 'success'
            return {
                "message":message,
                "status":status
            }

        except Exception as e:
            return {
                "message":str(e),
                "status":"error",
                "data":''
            }

    @staticmethod
    def delete_data_operation(table_name, row_id):
        connection = Dbconnect.dbconnects()
        if connection:
            try:
                cursor = connection.cursor()
                # if not isinstance(row_id, int):
                #     return {'status': 'Error', 'message': 'Row ID must be an integer'}

                delete_sql = f"DELETE FROM {table_name} WHERE id = '{row_id}'"
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
        # import pdb
        # pdb.set_trace()
        try:
            connection = Dbconnect.dbconnects()
            if connection:
                data_df = pd.DataFrame([column_data])
                set_clause = ', '.join([f"{key} = '{value}'" for key, value in column_data.items()])
                update_query = f"UPDATE {table_name} SET {set_clause} WHERE id = '{row_id}'"
                cursor = connection.cursor()
                cursor.execute(update_query)
                connection.commit()
                if cursor.rowcount > 0:
                    return {'status': 'success', 'message': 'Updated successfully'}
                else:
                    return {'status': 'error', 'message': 'No rows were updated'}
            else:
                return {'status': 'error', 'message': 'Failed to connect to the database'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

