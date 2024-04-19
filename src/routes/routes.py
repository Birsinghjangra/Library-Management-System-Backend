from flask import jsonify

from src.DataTransfer_job.data_transfer_jobs import DataTransfer
from src.bill_payment.bill_payment import Bill_payments
from src.fetchParameter.fetchparameter import Fetchparameters
from src.login.login import Login
from src.products.products import Product


class Routes:
    @staticmethod
    def addproduct(request):
        fetch_params = Fetchparameters()
        id = fetch_params.fetch_parameter(request, 'id', type=int)
        category = fetch_params.fetch_parameter(request, 'category', type=str)
        category_id = fetch_params.fetch_parameter(request, 'category_id', type=int)
        product_id = fetch_params.fetch_parameter(request, 'product_id', type=int)
        quantity = fetch_params.fetch_parameter(request, 'quantity', type=int)
        productName = fetch_params.fetch_parameter(request, 'productName', type=str)
        costPrice = fetch_params.fetch_parameter(request, 'costPrice', type=int)
        manufacturingDate = fetch_params.fetch_parameter(request, 'manufacturingDate', type=str)
        expiryDate = fetch_params.fetch_parameter(request, 'expiryDate', type=str)

        if id is not None:
            print(id)
            result = Product.update_product(id, category,category_id,product_id, quantity, productName, costPrice, manufacturingDate,expiryDate)
        else:
            result = Product.save_product(category,category_id,product_id, quantity, productName, costPrice, manufacturingDate, expiryDate)
        return result

    @staticmethod
    def get_product(request):
        fetch_params = Fetchparameters()
        id = fetch_params.fetch_parameter(request, 'id', type=int)
        result = Product().get_product_by_id(id)
        return result


    @staticmethod
    def get_products():
        return Product.get_products()

    @staticmethod
    def db_operations(request):
        fetch_params = Fetchparameters()
        id = fetch_params.fetch_parameter(request, 'id', type=int)
        table_name = fetch_params.fetch_parameter(request, 'table_name', type=str)
        action_mode = fetch_params.fetch_parameter(request,'action')

        if action_mode =="create":
            sql_insert = fetch_params.fetch_parameter(request, 'sql_insert')
            result = DataTransfer.create_data_operation(id,table_name,sql_insert)
        elif action_mode == "delete":
            row_ids = fetch_params.fetch_parameter(request, 'row_ids', )
            result = DataTransfer.delete_data_operation(table_name, row_ids)
        else:
            column_data = fetch_params.fetch_parameter(request, 'column_data')
            result = DataTransfer.save_data_operation(table_name, column_data, action_mode)
        return result



    @staticmethod
    def login_api(request):
        fetch_params = Fetchparameters()
        email = fetch_params.fetch_parameter(request, 'email', type=str)
        password= fetch_params.fetch_parameter(request,'password',type= str)
        return Login.login_api(email,password)

    @staticmethod
    def sell_product(request):
        fetch_params= Fetchparameters()
        id = fetch_params.fetch_parameter(request, 'product_id', type=int)
        sell_quantity=fetch_params.fetch_parameter(request, 'sell_quantity', type=int)
        unit_sellingPrice = fetch_params.fetch_parameter(request, 'unit_sellingPrice', type=int)
        return DataTransfer.sell_product(id,sell_quantity,unit_sellingPrice)


    @staticmethod
    def get_category_name(request):
        fetch_params= Fetchparameters()
        Table_name = fetch_params.fetch_parameter(request, 'Table_name', type=str)
        return Product.get_category_id(Table_name)

    @staticmethod
    def get_products_by_category(request):
        fetch_params = Fetchparameters()
        category_id = fetch_params.fetch_parameter(request, 'category_id', type=str)
        return Product.get_products_name(category_id)

    @staticmethod
    def save_order(request):
        fetch_params = Fetchparameters()
        name = fetch_params.fetch_parameter(request,'name', type = str)
        mobile = fetch_params.fetch_parameter(request, 'mobile', type=str)
        data = request.get_json()
        orders = data["orders"]
        result = Bill_payments.save_orders(name,mobile,orders)
        return result




