import os
import glob
from flask import jsonify, send_file

from src.DataTransfer_job.data_transfer_jobs import DataTransfer
from src.Get_data.get_data import GetData
from src.data_migration.borrower import Borrower
from src.fetchParameter.fetchparameter import Fetchparameters
from src.login.login import Login


class Routes:
    @staticmethod
    def db_operations(request):
        id = Fetchparameters.fetch_parameter(request, 'id', type=int)
        table_name = Fetchparameters.fetch_parameter(request, 'table_name', type=str)
        action_mode = Fetchparameters.fetch_parameter(request,'action')

        if action_mode =="create":
            sql_insert = Fetchparameters.fetch_parameter(request, 'sql_insert')
            result = DataTransfer.create_data_operation(id,table_name,sql_insert)
        elif action_mode == "delete":
            row_ids = Fetchparameters.fetch_parameter(request, 'row_ids', type=str )
            result = DataTransfer.delete_data_operation(table_name, row_ids)
        elif action_mode == "update":
            row_ids = Fetchparameters.fetch_parameter(request, 'id')
            column_data = Fetchparameters.fetch_parameter(request, 'column_data')
            result = DataTransfer.update_data_operation(row_ids, column_data, table_name)
        else:
            column_data = Fetchparameters.fetch_parameter(request, 'column_data')
            result = DataTransfer.save_data_operation(table_name, column_data, action_mode)
        return result



    @staticmethod
    def login_api(request):
        email = Fetchparameters.fetch_parameter(request, 'email', type=str)
        password= Fetchparameters.fetch_parameter(request,'password',type= str)
        return Login.login_api(email,password)

    # @staticmethod
    # def add_borrower(request):
    #
    #     query = "select count(card_id) + 1 from borrower;"
    #     prefix = 'ID'
    #     cursor.execute(query)
    #     row = cursor.fetchone()
    #     temp = str(row[0])
    #     card_id_temp = ''
    #     for i in range(len(temp), 6):
    #         card_id_temp = card_id_temp + '0'
    #     card_id = prefix + card_id_temp + temp
    #     query = "INSERT into BORROWER(card_id,ssn,bname,address,phone) values(%s,%s,%s,%s,%s)"
    #     response = None
    #     try:
    #         cursor.execute(query, (card_id, data["ssn"], data["name"], data["address"], data["phone"]))
    #         response = {'message': 'Borrower Added', 'success': True}
    #         cnx.commit()
    #     except mysql.connector.Error as err:
    #         if (err.errno in errorCodes.errorCodeMessage):
    #             response = {'message': errorCodes.errorCodeMessage[err.errno], 'success': False}
    #         else:
    #             response = {'message': 'Borrower Creation failed', 'success': False}
    #     return jsonify(response)

    @staticmethod
    def csv_import(request):
        return Login.csv_import()

    @staticmethod
    def addBorrower(request):
        # card_id = Fetchparameters.fetch_parameter(request, 'card_id', type=str)
        Ssn = Fetchparameters.fetch_parameter(request, 'Ssn', type=str)
        Bname = Fetchparameters.fetch_parameter(request, 'Bname', type=str)
        Address = Fetchparameters.fetch_parameter(request, 'Address', type=str)
        Phone =  Fetchparameters.fetch_parameter(request, 'Phone', type=str)
        result = Borrower.addBorrower(Ssn,Bname,Address,Phone)
        return result

    @staticmethod
    def getData_common(request):
        id = Fetchparameters.fetch_parameter(request,'id', type = str)
        Table_name = Fetchparameters.fetch_parameter(request, 'Table_name', type=str)
        result = GetData.getData_common(id,Table_name)
        return result

    @staticmethod
    def searchUser(request):
        id = Fetchparameters.fetch_parameter(request,'id', type = str)
        Table_name = Fetchparameters.fetch_parameter(request, 'Table_name', type=str)
        result = GetData.searchUser(id,Table_name)
        return result

    @staticmethod
    def searchBook(request):
        title = Fetchparameters.fetch_parameter(request,'title', type = str)
        Table_name = Fetchparameters.fetch_parameter(request, 'Table_name', type=str)
        result = GetData.searchBook(title,Table_name)
        return result

    @staticmethod
    def issue_book(request):
        id = Fetchparameters.fetch_parameter(request,'id',type = str)
        Isbn = Fetchparameters.fetch_parameter(request, 'Isbn', type =str)
        result = GetData.issue_book(id, Isbn)
        return result

    @staticmethod
    def calculate_fine(request):
        id = Fetchparameters.fetch_parameter(request, 'id', type=str)
        Isbn = Fetchparameters.fetch_parameter(request, 'Isbn', type=str)
        result = GetData.calculate_fine(id, Isbn)
        return result

    @staticmethod
    def submit_fine(request):
        id = Fetchparameters.fetch_parameter(request, 'id', type=str)
        Isbn = Fetchparameters.fetch_parameter(request, 'Isbn', type=str)
        result = GetData.submit_fine(id, Isbn)
        return result

    @staticmethod
    def allUserBook(request):
        id = Fetchparameters.fetch_parameter(request, 'id', type=str)
        Isbn = Fetchparameters.fetch_parameter(request, 'Isbn',default='0', type=str)
        result = GetData.allUserBook(id,Isbn)
        return result

    @staticmethod
    def generateBarCode(request):
        from src.data_migration.barcode import BarcodeGenerator
        # bookName = Fetchparameters.fetch_parameter(request, 'bookName', type=str)
        # edition = Fetchparameters.fetch_parameter(request, 'edition', type=str)
        # author = Fetchparameters.fetch_parameter(request, 'author', type=str)
        isbn = Fetchparameters.fetch_parameter(request, 'isbn', type=str)
        if not isbn:
            return jsonify({"error": "ISBN is required"}), 400
        # barcode_path, error_response, status_code = BarcodeGenerator.generate_barcode(isbn)
        # if error_response:
        #     return error_response, status_code
        # return send_file(
        #     barcode_path,
        #     as_attachment=True,
        #     download_name=f"barcode_{isbn}.png",  # Customize the filename
        #     mimetype='image/png'  # Set the MIME type
        # )

        result = BarcodeGenerator.generate_barcode(isbn)
        return result

    @staticmethod
    def download_barcode(request):
        from app import SAVE_DIR
        isbn = Fetchparameters.fetch_parameter(request, 'isbn', type=str)
        if not isbn:
            return jsonify({"error": "ISBN parameter is required."}), 400

        try:
            barcode_path = os.path.join(SAVE_DIR, f"{isbn}.png")
            absolute_path = os.path.abspath(barcode_path)

            print(f"Looking for barcode at: {absolute_path}")  # Debug print
            if not os.path.exists(absolute_path):
                return jsonify({"message": "Barcode not found.", "status": "error"}), 404

            return send_file(absolute_path, as_attachment=True, download_name=f"{isbn}.png", mimetype='image/png')

        except Exception as e:
            print(f"Error: {str(e)}")  # Debug print
            return jsonify({"error": str(e)}), 500
