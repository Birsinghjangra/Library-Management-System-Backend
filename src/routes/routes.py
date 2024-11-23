import io
import os
from fpdf import FPDF
import pandas as pd
from flask import jsonify, send_file
from io import BytesIO
import pandas as pd
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from src.DB_connect.dbconnection import Dbconnect

from src.DB_connect.dbconnection import Dbconnect
from src.DataTransfer_job.data_transfer_jobs import DataTransfer
from src.Get_data.get_data import GetData
from src.csv_uploads.csv_upload import Csv_upload
from src.data_migration.table_data import TableData
from src.fetchParameter.fetchparameter import Fetchparameters
from src.jobs.submitBook import SubmitBook
from src.login.login import Login
from src.report.report import Generatereport


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
        result = TableData.addStudent(srn, student_name, class_, section, roll_no, phone, address)
        return result

    @staticmethod
    def addBook(request):
        isbn = Fetchparameters.fetch_parameter(request, 'isbn', type=str)
        title = Fetchparameters.fetch_parameter(request, 'title', type=str)
        publication = Fetchparameters.fetch_parameter(request, 'publication', type=str)
        author_name = Fetchparameters.fetch_parameter(request, 'author_name', type=str)
        price = Fetchparameters.fetch_parameter(request, 'price', type=str)
        edition = Fetchparameters.fetch_parameter(request, 'edition', type=str)
        quantity = Fetchparameters.fetch_parameter(request, 'quantity', type=str)
        result = TableData.addStudent(isbn, title, publication, author_name, price, edition, quantity)
        return result

    @staticmethod
    def getData_common(request):
        id = Fetchparameters.fetch_parameter(request, 'id', type=str)
        srn = Fetchparameters.fetch_parameter(request,'srn', type = str)
        Table_name = Fetchparameters.fetch_parameter(request, 'Table_name', type=str)
        result = GetData.getData_common(id,srn,Table_name)
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
        Isbn = Fetchparameters.fetch_parameter(request, 'isbn', type=str)
        book_id = Fetchparameters.fetch_parameter(request, 'book_id', type=str)
        srn = Fetchparameters.fetch_parameter(request, 'srn', type=str)
        isDamage = Fetchparameters.fetch_parameter(request, 'isDamage', type=str)
        result = GetData.calculate_fine(srn,id, Isbn,book_id,isDamage)
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
        isbn = Fetchparameters.fetch_parameter(request, 'isbn', type=str)
        if not isbn:
            return jsonify({"error": "ISBN is required"}), 400

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

    @staticmethod
    def sidebar_menu_config(request):
        AccountId = Fetchparameters.fetch_parameter(request, 'id', type=str)
        return GetData.sidebar_menu_config(AccountId)

    @staticmethod
    def submit_book(request):
        srn = Fetchparameters.fetch_parameter(request, 'srn', type=str)
        book_id = Fetchparameters.fetch_parameter(request, 'book_id', type=str)
        isbn = Fetchparameters.fetch_parameter(request, 'isbn', type=str)
        isDamage = Fetchparameters.fetch_parameter(request, 'isDamage', type=str)
        isLost = Fetchparameters.fetch_parameter(request, 'isLost', type=str)
        return SubmitBook.submit_book(srn,book_id,isbn,isDamage,isLost)

    @staticmethod
    def toggleStatus(request):
        srn = Fetchparameters.fetch_parameter(request, 'srn', type=str)
        book_id = Fetchparameters.fetch_parameter(request, 'book_id', type=str)
        return DataTransfer.toggleStatus(srn, book_id)

    @staticmethod
    def getreport(request):
        query = Fetchparameters.fetch_parameter(request, 'query', type=str)
        return Generatereport.getreportdata(query)

    @staticmethod
    def exportreport(request):
        # Fetch query and format from request
        query = Fetchparameters.fetch_parameter(request, 'query', type=str)
        report_format = Fetchparameters.fetch_parameter(request, 'format', type=str)

        try:
            # Log received query and format
            print(f"Received query: {query}, format: {report_format}")

            # Fetch data from the database directly using the query
            connection = Dbconnect.dbconnects()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            print(f"Query result: {result}")

            # Convert the result to a pandas DataFrame
            df = pd.DataFrame(result)
            print("DataFrame created successfully")

            if report_format == 'pdf':
                # Generate PDF from the DataFrame
                buffer = BytesIO()
                c = canvas.Canvas(buffer, pagesize=letter)
                page_width, page_height = letter

                # Calculate dynamic column widths based on content
                column_widths = []
                for col in df.columns:
                    max_length = max([len(str(col))] + [len(str(value)) for value in df[col]])
                    column_width = max_length * 10
                    column_widths.append(column_width)

                # Ensure total width does not exceed the page width
                total_table_width = sum(column_widths)
                if total_table_width > (page_width - 100):  # Allow for margins
                    scaling_factor = (page_width - 100) / total_table_width
                    column_widths = [int(width * scaling_factor) for width in column_widths]

                # Set initial positions
                x_start = 30  # Left margin
                y_position = page_height - 50  # Start below the top margin
                row_height = 20  # Height of each row
                cell_margin = -8  # Top margin for cell data

                # Add Title (centered)
                c.setFont("Helvetica-Bold", 14)
                title_text = "Exported Report"
                title_width = c.stringWidth(title_text, "Helvetica-Bold", 14)
                c.drawString((page_width - title_width) / 2, y_position + 10, title_text)  # Center the title
                y_position -= 1  # Adjust y_position for title margin

                # Draw Table Headers
                c.setFont("Helvetica-Bold", 10)
                for col_idx, col_name in enumerate(df.columns):
                    x_center = x_start + (column_widths[col_idx] / 2)
                    y_center = y_position - row_height / 2 + 5 + cell_margin
                    c.drawCentredString(x_center, y_center, str(col_name))  # Apply y_offset to text
                    c.rect(x_start, y_position - row_height, column_widths[col_idx], row_height, fill=0, stroke=1)
                    x_start += column_widths[col_idx]

                y_position -= row_height
                x_start = 30  # Reset to start of the table

                # Draw Table Rows
                c.setFont("Helvetica", 10)
                for _, row in df.iterrows():
                    for col_idx, col_name in enumerate(df.columns):
                        text = str(row[col_name])
                        x_center = x_start + (column_widths[col_idx] / 2)
                        y_center = y_position - row_height / 2 + 5 + cell_margin
                        c.drawCentredString(x_center, y_center, text)  # Apply margin top to cell text
                        c.rect(x_start, y_position - row_height, column_widths[col_idx], row_height, fill=0, stroke=1)
                        x_start += column_widths[col_idx]

                    y_position -= row_height
                    x_start = 30  # Reset to start of the row

                    # Check for page overflow
                    if y_position < 50:  # Bottom margin
                        c.showPage()
                        c.setFont("Helvetica", 10)
                        y_position = page_height - 50  # Reset position
                        x_start = 30  # Reset start position

                        # Redraw Headers on New Page
                        for col_idx, col_name in enumerate(df.columns):
                            x_center = x_start + (column_widths[col_idx] / 2)
                            y_center = y_position - row_height / 2 + 5
                            c.drawCentredString(x_center, y_center, str(col_name))  # Apply y_offset to text
                            c.rect(x_start, y_position - row_height, column_widths[col_idx], row_height, fill=0, stroke=1)
                            x_start += column_widths[col_idx]

                        y_position -= row_height
                        x_start = 30  # Reset to start of the row

                # Save and send the PDF
                c.save()
                buffer.seek(0)
                return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='report.pdf')

            elif report_format == 'xlsx':
                # Generate Excel file from the DataFrame
                buffer = BytesIO()
                df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                return send_file(buffer, mimetype='application/vnd.ms-excel', as_attachment=True, download_name='report.xlsx')

            else:
                return {'message': 'Invalid format specified'}, 400

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return {'message': f'Internal server error: {str(e)}'}, 500
