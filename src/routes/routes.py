from flask import jsonify

from src.DataTransfer_job.data_transfer_jobs import DataTransfer
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
            row_ids = Fetchparameters.fetch_parameter(request, 'row_ids', )
            result = DataTransfer.delete_data_operation(table_name, row_ids)
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

        return Login.csv_import()

    @staticmethod
    def addBorrower(request):
        card_id = Fetchparameters.fetch_parameter(request, 'card_id', type=int)
        result = Borrower.addBorrower(card_id)
        return result

