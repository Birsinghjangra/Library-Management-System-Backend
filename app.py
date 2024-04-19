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
    db_connection = Dbconnect()
    connection = db_connection.dbconnects()
    if connection:
        return 'Connected to MySQL database'
    else:
        return 'Failed to connect to MySQL database'

@app.route('/addproduct', methods=METHODS)
def add_product():
    return Routes.addproduct(request)

@app.route('/getproducts', methods=METHODS)
def get_products():
    return Routes.get_products()

@app.route('/get_productby_id', methods=METHODS)
def get_product():
    return Routes.get_product(request)

@app.route('/getdata_for_all', methods= METHODS)
def get_category():
    return Routes.get_category_name(request)

@app.route('/db_operation', methods=METHODS)
def db_operations():
    return Routes.db_operations(request)

@app.route('/get_products_by_category',methods=METHODS)
def get_products_by_category():
    return Routes.get_products_by_category(request)

@app.route('/product_sales',methods=METHODS)
def product_sells():
    return Routes.sell_product(request)

@app.route('/login',methods=METHODS)
def login_api():
    return Routes.login_api(request)


if __name__ == '__main__':
    app.run(debug=True)
