import mysql

from src.DB_connect.dbconnection import Dbconnect
from src.data_migration.table_data import TableData


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
                result = TableData.addStudent(column_data)
                return result

            if table_name == 'book':
                result = TableData.addBook(column_data)
                return result

            # if connection:
            #     # Extract quantity from column_data if available
            #     quantity = column_data.get('quantity', 1)  # Default to 1 if not specified
            #     # Remove quantity from column_data to avoid insertion into the database
            #     column_data.pop('quantity', None)
            #
            #     # Prepare a list to hold data for multiple rows
            #     data_to_insert = []
            #
            #     # Validate quantity
            #     if quantity is None or quantity < 1:
            #         return {
            #             "message": "Quantity must be at least 1.",
            #             "status": "error"
            #         }
            #
            #     for i in range(quantity):
            #         # Create a copy of the data to insert
            #         row_data = column_data.copy()  # Make a copy to avoid overwriting
            #
            #         # Set quantity to 1 for each row
            #         row_data['quantity'] = 1  # Set quantity to 1 for each row
            #         data_to_insert.append(row_data)
            #
            #     # Normalize the data and create a DataFrame
            #     data_set = pd.json_normalize(data_to_insert)
            #     Dataframe_pandas.write_df_to_sql(data_set, table_name, operation='REPLACE')
            #
            #     if validation_flag == 1:
            #         message = 'Fields have an Empty Value'
            #         status = "error"
            #     else:
            #         message = 'Books added successfully'
            #         status = 'success'
            #
                # return {
                #     "message": message,
                #     "status": status
                # }

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

            # Create the SET clause by joining the column names with placeholders
            set_clause = ', '.join([f"{key} = %s" for key in column_data.keys()])

            # Determine the table-specific WHERE clause
            if table_name == "book":
                update_query = f"UPDATE {table_name} SET {set_clause} WHERE book_id = %s"
            elif table_name == "student":
                update_query = f"UPDATE {table_name} SET {set_clause} WHERE srn = %s"
            else:
                update_query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"

            # Prepare the list of values, including the row_id at the end
            values = list(column_data.values()) + [row_id]

            # Execute the query with the correct parameters
            cursor = connection.cursor()
            cursor.execute(update_query, values)
            connection.commit()

            # Return a success message without checking for rows updated
            return {'status': 'success', 'message': 'Update operation completed'}

        except Exception as e:
            return {'status': 'error', 'message': f"An error occurred: {str(e)}"}

    @staticmethod
    def toggleStatus(srn=None, book_id=None):
        try:
            connection = Dbconnect.dbconnects()
            if not connection:
                return {'status': 'error', 'message': 'Failed to connect to the database'}

            cursor = connection.cursor()

            if srn:
                # Toggle for student
                select_query = "SELECT isActive FROM student WHERE srn = %s"
                cursor.execute(select_query, (srn,))
                result = cursor.fetchone()

                if not result:
                    return {'status': 'error', 'message': 'Student not found'}, 404

                current_status = result[0]
                new_status = 0 if current_status == 1 else 1

                # Update the isActive field for the student
                update_query = "UPDATE student SET isActive = %s WHERE srn = %s"
                cursor.execute(update_query, (new_status, srn))
                connection.commit()

                return {
                           'message': f'Student with SRN {srn} isActive status toggled to {new_status}',
                           'srn': srn,
                           'new_status': new_status
                       }, 200

            elif book_id:
                # Toggle for book
                select_query = "SELECT isActive FROM book WHERE book_id = %s"
                cursor.execute(select_query, (book_id,))
                result = cursor.fetchone()

                if not result:
                    return {'status': 'error', 'message': 'Book not found'}, 404

                current_status = result[0]
                new_status = 0 if current_status == 1 else 1

                # Update the isActive field for the book
                update_query = "UPDATE book SET isActive = %s WHERE book_id = %s"
                cursor.execute(update_query, (new_status, book_id))
                connection.commit()

                return {
                           'message': f'Book with ID {book_id} isActive status toggled to {new_status}',
                           'book_id': book_id,
                           'new_status': new_status
                       }, 200

            else:
                return {'status': 'error', 'message': 'Either SRN or Book ID is required'}, 400

        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

        finally:
            if 'cursor' in locals():
                cursor.close()
            if connection:
                connection.close()
