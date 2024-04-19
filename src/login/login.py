from src.DB_connect.dbconnection import Dbconnect


class Login:

    @staticmethod
    def login_api(email,password):
        from src.DB_connect.dbconnection import Dbconnect
        db_connection = Dbconnect()
        connection =db_connection.dbconnects()
        if connection:
            try:
                cursor = connection.cursor()
                query = f"""SELECT * FROM signup WHERE email = '{email}' AND password = '{password}'"""
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    return {
                        "data":result,
                        "message":"login succesful",
                        "status":"success"
                    }
                else:
                    return {"data":[],
                        "message":"invalid credentials",
                            "status":"error"}
            except Exception as e:
                return {"error": str(e)}
            finally:
                # Close cursor and database connection
                cursor.close()
                connection.close()
        else:
            # Failed to connect to the database
            return {"error": "Failed to connect to the database"}




