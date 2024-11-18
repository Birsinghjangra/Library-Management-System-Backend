import requests
from flask import Flask, request,send_file, jsonify  # Import request object
from flask_cors import CORS
import os
# from src.routes.routes import Routes
from src.DB_connect.dbconnection import Dbconnect
from src.config import SECRET_KEY
from src.routes.routes import Routes
from src.app_decorator.app_decorator import app_decorator

METHODS = ['GET', 'POST']

app = Flask(__name__)
SAVE_DIR = 'barcodes'

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx','.xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB file size limit

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
app.config['SECRET_KEY'] = SECRET_KEY['secret_key']
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
@app_decorator
def db_operations():
    return Routes.db_operations(request)

@app.route('/login',methods=METHODS)
def login_api():
    return Routes.login_api(request)

@app.route('/csv_import',methods=METHODS)
# @app.route('/csvimport',methods=METHODS)
# @app_decorator
def csv_import():
    return Routes.csv_import(request)

@app.route("/addStudent",methods=METHODS)
@app_decorator
def addStudent():
    return Routes.addStudent(request)

@app.route("/toggleStatus",methods=METHODS)
# @app_decorator
def toggleStatus():
    return Routes.toggleStatus(request)

@app.route("/getData_common",methods=METHODS)
@app_decorator
def getdata():
    return Routes.getData_common(request)

@app.route("/searchUser",methods=METHODS)
@app_decorator
def getuser():
    return Routes.searchUser(request)

@app.route("/searchBook",methods=METHODS)
@app_decorator
def getbook():
    return Routes.searchBook(request)

@app.route("/issue_book",methods =METHODS)
@app_decorator
def issue_book():
    return Routes.issue_book(request)

@app.route("/calculate_fine",methods =METHODS)
@app_decorator
def calculate_fine():
    return Routes.calculate_fine(request)

@app.route("/submit_fine",methods =METHODS)
@app_decorator
def submit_fine():
    return Routes.submit_fine(request)

@app.route("/allUserBook",methods =METHODS)
@app_decorator
def allUserBook():
    return Routes.allUserBook(request)

@app.route("/generateBarCode",methods =METHODS)
@app_decorator
def generateBarCode():
    return Routes.generateBarCode(request)

@app.route('/download_Barcode', methods=METHODS)
@app_decorator
def download_barcode():
    return Routes.download_barcode(request)

@app.route('/return_issue_book', methods= METHODS)
@app_decorator
def return_book():
    return Routes.return_book(request)

@app.route('/sidebarMenuConfig', methods = METHODS)
@app_decorator
def sidebar_menu_config():
    return Routes.sidebar_menu_config(request)

@app.route('/submitbook', methods = METHODS)
@app_decorator
def submit_book():
    return Routes.submit_book(request)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)

