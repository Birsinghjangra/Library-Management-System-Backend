import requests
from flask import Flask, request, jsonify  # Import request object
from flask_cors import CORS

# from src.routes.routes import Routes

from src.DB_connect.dbconnection import Dbconnect
from src.routes.routes import Routes

METHODS = ['GET', 'POST']

app = Flask(__name__)
CORS(app)

@app.route('/mysql', methods=METHODS)
def connectionss():
    connection = Dbconnect.dbconnects()
    if connection:
        print('Connected to MySQL database')
        return 'Connected to MySQL database'
    else:
        print('Failed to connect to MySQL database')
        return 'Failed to connect to MySQL database'

@app.route('/db_operation', methods=METHODS)
def db_operations():
    return Routes.db_operations(request)

@app.route('/login',methods=METHODS)
def login_api():
    return Routes.login_api(request)

@app.route('/csvimport',methods=METHODS)
def csv_import():
    return Routes.csv_import(request)

@app.route("/addBorrower",methods=METHODS)
def addBorrower1():
    return Routes.addBorrower(request)

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
# @app.route("/addBorrower",methods=METHODS)
# def addBorrower():
#     data = request.get_json(force=True)
#     query = "select count(card_id) + 1 from borrower;"
#     prefix = 'ID'
#     cursor.execute(query)
#     row = cursor.fetchone()
#     temp = str(row[0])
#     card_id_temp = ''
#     for i in range(len(temp),6):
#         card_id_temp = card_id_temp + '0'
#     card_id = prefix+card_id_temp+temp
#     query = "INSERT into BORROWER(card_id,ssn,bname,address,phone) values(%s,%s,%s,%s,%s)"
#     response = None
#     try:
#         cursor.execute(query,(card_id,data["ssn"],data["name"],data["address"],data["phone"]))
#         response = {'message':'Borrower Added','success':True}
#         connection.commit()
#     except mysql.connector.Error as err:
#         if(err.errno in errorCodes.errorCodeMessage):
#             response = {'message':errorCodes.errorCodeMessage[err.errno],'success':False}
#         else:
#             response = {'message':'Borrower Creation failed','success':False}
#     return jsonify(response)
#

if __name__ == '__main__':
    app.run(debug=True)
