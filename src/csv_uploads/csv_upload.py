import pandas as pd
from datetime import datetime
from src.DB_connect.dbconnection import Dbconnect

class Csv_upload:
    @staticmethod
    def csv_import(file_name, table_name):
        try:
            # Load the file into a DataFrame
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_name)
            elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
                df = pd.read_excel(file_name)
            else:
                return {
                    "status": "error",
                    "message": "File must be a CSV or Excel file"
                }

            connection = Dbconnect.dbconnects()
            cursor = connection.cursor()

            if table_name == 'student':
                # Prepare INSERT for student
                insert_sql = """
                    INSERT INTO `student` 
                    (`srn`, `student_name`, `class`, `section`, `roll_no`, `phone`, `address`, `createdOn`, `isActive`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                rows_to_insert = []

                for _, row in df.iterrows():
                    student_data = row.to_dict()
                    # Validation for required fields
                    if pd.isnull(student_data.get('srn')) or pd.isnull(student_data.get('student_name')) or \
                       pd.isnull(student_data.get('class')) or pd.isnull(student_data.get('section')) or \
                       pd.isnull(student_data.get('roll_no')) or pd.isnull(student_data.get('phone')) or \
                       pd.isnull(student_data.get('address')):
                        return {
                            "status": "error",
                            "message": "One or more required fields (`srn`, `student_name`, `class`, `section`, `roll_no`, `phone`, `address`) are missing."
                        }
                    rows_to_insert.append((
                        student_data['srn'],
                        student_data['student_name'],
                        student_data['class'],
                        student_data['section'],
                        student_data['roll_no'],
                        student_data['phone'],
                        student_data['address'],
                        student_data.get('createdOn', datetime.now().strftime('%Y-%m-%d')),  # Default to today
                        student_data.get('isActive', 1)  # Default to 1
                    ))

                skipped_rows = []
                for row in rows_to_insert:
                    try:
                        cursor.execute(insert_sql, row)
                    except Exception as e:
                        if "Duplicate entry" in str(e):  # Handle duplicate SRN or unique constraint
                            skipped_rows.append(row[0])  # Log the SRN of the skipped row
                        else:
                            raise e

            elif table_name == 'book':
                # Prepare INSERT for book
                insert_sql = """
                    INSERT INTO `book` 
                    (`isbn`, `title`, `publication`, `author_name`, `price`, `edition`, `quantity`, `isCheckedOut`, `srn`, `isActive`, `createdOn`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                rows_to_insert = []

                for _, row in df.iterrows():
                    book_data = row.to_dict()
                    # Validation for required fields
                    if pd.isnull(book_data.get('isbn')) or pd.isnull(book_data.get('title')) or \
                       pd.isnull(book_data.get('publication')) or pd.isnull(book_data.get('author_name')) or \
                       pd.isnull(book_data.get('price')) or pd.isnull(book_data.get('edition')):
                        return {
                            "status": "error",
                            "message": "One or more required fields (`isbn`, `title`, `publication`, `author_name`, `price`, `edition`) are missing."
                        }
                    quantity = int(book_data.get('quantity', 1))
                    for _ in range(quantity):  # Create multiple rows based on quantity
                        rows_to_insert.append((
                            book_data['isbn'],
                            book_data['title'],
                            book_data['publication'],
                            book_data['author_name'],
                            book_data['price'],
                            book_data['edition'],
                            1,  # Quantity is always 1 for each row
                            0,  # isCheckedOut default
                            book_data.get('srn'),
                            book_data.get('isActive', 1),  # Default to 1
                            book_data.get('createdOn', datetime.now().strftime('%Y-%m-%d'))  # Default to today
                        ))

                skipped_rows = []
                for row in rows_to_insert:
                    try:
                        cursor.execute(insert_sql, row)
                    except Exception as e:
                        if "Duplicate entry" in str(e):  # Handle duplicate ISBN
                            skipped_rows.append(row[0])  # Log the ISBN of the skipped row
                        else:
                            raise e

            else:
                return {
                    "status": "error",
                    "message": f"Table `{table_name}` is not supported."
                }

            connection.commit()
            return {
                "status": "success",
                "message": f"{len(rows_to_insert) - len(skipped_rows)} rows inserted into the `{table_name}` table.",
                "skipped_rows": skipped_rows  # Optionally include skipped rows
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
