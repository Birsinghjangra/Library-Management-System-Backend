import mysql.connector

class Dbconnect:
    @staticmethod
    def dbconnects():
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='admin123',
            database ="lms"
        )
        return connection