from src.DB_connect.dbconnection import Dbconnect
from datetime import datetime

class Borrower:
    @staticmethod
    def addborower(column_data):

        Bname = column_data['Bname']
        Address = column_data['Address']
        Phone = column_data['Phone']
        date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection = Dbconnect.dbconnects()
        if connection:
            cursor = connection.cursor()
            try:
                query = "select count(id) + 1 from borrower;"
                prefix = 'ID'
                cursor.execute(query)
                row = cursor.fetchone()
                temp = str(row[0])
                card_id_temp = ''
                for i in range(len(temp), 6):
                    card_id_temp = card_id_temp + '0'
                card_id = prefix + card_id_temp + temp
                query1 = f"INSERT INTO BORROWER (id, Bname, Address, Phone, date_added) VALUES ('{card_id}', '{Bname}', '{Address}', '{Phone}', '{date_added}')"
                print(query1)
                response = None
                cursor.execute(query1)
                response = {'message': 'Borrower Added successfully', 'status': 'success'}
                connection.commit()
                return response
            except Exception as e:
                return {'message': str(e),
                        'status': 'error'}