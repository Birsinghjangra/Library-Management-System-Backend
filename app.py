import requests
from flask import Flask, request,send_file, jsonify  # Import request object
from flask_cors import CORS
import os
# from src.routes.routes import Routes

from src.DB_connect.dbconnection import Dbconnect
from src.routes.routes import Routes

METHODS = ['GET', 'POST']

app = Flask(__name__)
SAVE_DIR = 'barcodes'

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx','.xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 16 MB file size limit

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/mysql', methods=METHODS)
def connectionss():
    connection = Dbconnect.dbconnects()
    if connection:
        # print('Connected to MySQL database')
        return 'Connected to MySQL database'
    else:
        # print('Failed to connect to MySQL database')
        return 'Failed to connect to MySQL database'

@app.route('/db_operation', methods=METHODS)
def db_operations():
    return Routes.db_operations(request)

@app.route('/login',methods=METHODS)
def login_api():
    return Routes.login_api(request)

@app.route('/csv_import',methods=METHODS)
def csv_import():
    return Routes.csv_import(request)

@app.route("/addStudent",methods=METHODS)
def addStudent():
    return Routes.addStudent(request)

@app.route("/getData_common",methods=METHODS)
def getdata():
    return Routes.getData_common(request)

@app.route("/searchUser",methods=METHODS)
def getuser():
    return Routes.searchUser(request)

@app.route("/searchBook",methods=METHODS)
def getbook():
    return Routes.searchBook(request)

@app.route("/issue_book",methods =METHODS)
def issue_book():
    return Routes.issue_book(request)

@app.route("/calculate_fine",methods =METHODS)
def calculate_fine():
    return Routes.calculate_fine(request)

@app.route("/submit_fine",methods =METHODS)
def submit_fine():
    return Routes.submit_fine(request)

@app.route("/allUserBook",methods =METHODS)
def allUserBook():
    return Routes.allUserBook(request)

@app.route("/generateBarCode",methods =METHODS)
def generateBarCode():
    return Routes.generateBarCode(request)

@app.route('/download_Barcode', methods=METHODS)
def download_barcode():
    return Routes.download_barcode(request)

@app.route('/return_issue_book', methods= METHODS)
def return_book():
    return Routes.return_book(request)

if __name__ == '__main__':
    app.run(debug=True)
