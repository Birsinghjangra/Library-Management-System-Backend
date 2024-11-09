import pandas as pd

from src.DB_connect.dbconnection import Dbconnect


class Csv_upload:
    @staticmethod
    def csv_import(file_name,table_name):
        try:
            print(file_name)
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_name)
            elif file_name.endswith(".xlsx"):
                df = pd.read_excel(file_name)
            elif file_name.endswith(".xls"):  # Corrected from .xlx to .xls
                df = pd.read_excel(file_name)
            else:
                return {
                    "status":"error",
                    "message":"File must be a CSV or Excel file"
                }

            def map_dtype_to_mysql(dtype):
                if pd.api.types.is_integer_dtype(dtype):
                    return "INT"
                elif pd.api.types.is_float_dtype(dtype):
                    return "FLOAT"
                elif pd.api.types.is_datetime64_any_dtype(dtype):
                    return "DATETIME"
                elif pd.api.types.is_string_dtype(dtype):
                    return "TEXT"
                else:
                    return "TEXT"  # Default to TEXT for unknown types
            connection = Dbconnect.dbconnects()
            cursor = connection.cursor()
            columns = ', '.join([f"`{col}` {map_dtype_to_mysql(df[col].dtype)}" for col in df.columns])
            create_table_sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns})"
            cursor.execute(create_table_sql)
            insert_sql = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
            rows = [tuple(x) for x in df.to_numpy()]
            cursor.executemany(insert_sql, rows)
            connection.commit()
            return {
                "status": "success",
                "message": f"Data uploaded to the {table_name}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
