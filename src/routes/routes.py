import os
import glob
from flask import jsonify, send_file

from src.DataTransfer_job.data_transfer_jobs import DataTransfer
from src.Get_data.get_data import GetData
from src.csv_uploads.csv_upload import Csv_upload
from src.data_migration.student import Student
from src.fetchParameter.fetchparameter import Fetchparameters
from src.login.login import Login

class Routes:
    @staticmethod
    def db_operations(request):
        srn = Fetchparameters.fetch_parameter(request, 'srn', type=int)
        table_name = Fetchparameters.fetch_parameter(request, 'table_name', type=str)
        action_mode = Fetchparameters.fetch_parameter(request,'action')

        if action_mode =="create":
            sql_insert = Fetchparameters.fetch_parameter(request, 'sql_insert')
            result = DataTransfer.create_data_operation(srn,table_name,sql_insert)
        elif action_mode == "delete":
            row_ids = Fetchparameters.fetch_parameter(request, 'row_ids', type=str )
            result = DataTransfer.delete_data_operation(table_name, row_ids)
        elif action_mode == "update":
            row_ids = Fetchparameters.fetch_parameter(request, 'srn')
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

    @staticmethod
    def csv_import(request):
        # file = Fetchparameters.fetch_parameter(request, 'file', type=str)
        file = request.files.get('file')
        table_name = Fetchparameters.fetch_parameter(request, 'table_name', type=str)
        if file is None:
            return jsonify({
                "status": "error",
                "message": "No file provided. Please upload a CSV or Excel file."
            }), 400
        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "No selected file. Please select a CSV or Excel file."
            }), 400
        if not file.filename.lower().endswith(('.csv', '.xlsx','.xls')):
            return jsonify({
                "status": "error",
                "message": "Invalid file type. Please upload a CSV or Excel file."
            }), 400
        file_path = f"./uploads/{file.filename}"
        file.save(file_path)

        result = Csv_upload.csv_import(file_path,table_name)
        return result


    @staticmethod
    def addStudent(request):
        srn = Fetchparameters.fetch_parameter(request, 'srn', type=str)
        student_name = Fetchparameters.fetch_parameter(request, 'student_name', type=str)
        class_ = Fetchparameters.fetch_parameter(request, 'class', type=str)
        section = Fetchparameters.fetch_parameter(request, 'section', type=str)
        roll_no = Fetchparameters.fetch_parameter(request, 'roll_no', type=str)
        phone = Fetchparameters.fetch_parameter(request, 'phone', type=str)
        address = Fetchparameters.fetch_parameter(request, 'address', type=str)
        result = Student.addStudent(srn, student_name, class_, section, roll_no, phone, address)
        return result

    @staticmethod
    def getData_common(request):
        id = Fetchparameters.fetch_parameter(request,'id', type = str)
        Table_name = Fetchparameters.fetch_parameter(request, 'Table_name', type=str)
        result = GetData.getData_common(id,Table_name)
        return result

    @staticmethod
    def searchUser(request):
        srn = Fetchparameters.fetch_parameter(request,'srn', type = str)
        Table_name = Fetchparameters.fetch_parameter(request, 'Table_name', type=str)
        result = GetData.searchUser(srn,Table_name)
        return result

    @staticmethod
    def searchBook(request):
        title = Fetchparameters.fetch_parameter(request,'title', type = str)
        isbn = Fetchparameters.fetch_parameter(request, 'isbn',default=" ''", type=str)
        Table_name = Fetchparameters.fetch_parameter(request, 'Table_name', type=str)
        result = GetData.searchBook(title, isbn,Table_name)
        return result

    @staticmethod
    def issue_book(request):
        srn = Fetchparameters.fetch_parameter(request,'srn',type = str)
        isbn = Fetchparameters.fetch_parameter(request, 'isbn', type =str)
        result = GetData.issue_book(srn, isbn)
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

    @staticmethod
    def return_book(request):
        srn = Fetchparameters.fetch_parameter(request, 'srn', type=str)
        return "hello"