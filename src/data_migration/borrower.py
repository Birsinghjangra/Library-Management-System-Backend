from src.DB_connect.dbconnection import Dbconnect


class Borrower:
    @staticmethod
    def addBorrower(card_id):
        connection = Dbconnect.dbconnects()
        if connection:
            cursor = connection.connect()
            try:
                query = "select count(card_id) + 1 from borrower;"
                prefix = 'ID'
                cursor.execute(query)
                row = cursor.fetchone()
                temp = str(row[0])
                card_id_temp = ''
                for i in range(len(temp),6):
                    card_id_temp = card_id_temp + '0'
                card_id = prefix+card_id_temp+temp
                query = "INSERT into BORROWER(card_id,ssn,bname,address,phone) values(%s,%s,%s,%s,%s)"
                response = None
                cursor.execute(query)
                response = {'message': 'Borrower Added', 'success': True}
                connection.commit()
                return response
            except Exception as e:
                return {"error": str(e)}