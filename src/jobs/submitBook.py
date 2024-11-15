import json
import logging

from src.DB_connect.dbconnection import Dbconnect
from src.dataframe_df.dataframe_operations import Dataframe_pandas


class SubmitBook:
    @staticmethod
    def submit_book(srn,book_id,isbn):
        try:
            query= f""" SELECT * FROM borrower_book_detail WHERE book_id = {book_id} AND isbn = {isbn} AND srn = {srn}"""
            df = Dataframe_pandas.read_sql_as_df(query)
            if df is not None and not df.empty:
                book_json = json.loads(df.to_json(orient='records'))
                for row in book_json:
                    book_id = row['id']
                    update_user_details= f"""UPDATE borrower_book_detail SET book_id = null, isbn = null
            WHERE id = {book_id}"""
                    update_book = f"""UPDATE book SET isCheckedOut = 0
            WHERE book_id = {book_id}"""
                    connection = Dbconnect.dbconnects()
                    cursor = connection.cursor()
                    cursor.execute(update_user_details)
                    cursor.execute(update_book)
                    connection.commit()
                    cursor.close()
                    connection.close()
                return {
                        "message": "Book returned successfully",
                        "status": "success",
                        "data": []
                    }
            else:
                return {
                    "message":"No book issued to this isbn",
                    "status":"error",
                    "data":[]
                }
        except Exception as e:
            # logging.DEBUG(f"""error is submit book {str(e)}""")
            return {
                "message": f"""{str(e)}""",
                "status": "error",
                "data": []

            }
