import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
class Dbconnect:
    @staticmethod
    def dbconnects():
        connection = mysql.connector.connect(
            host=os.getenv('HOST'),
            port=os.getenv('PORT'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE')
        )
        return connection