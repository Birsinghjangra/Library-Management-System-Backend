import json

from flask import jsonify

from src.dataframe_df.dataframe_operations import Dataframe_pandas


class Generatereport:
    @staticmethod
    def getreportdata(query):
        try:
            df = Dataframe_pandas.read_sql_as_df(query)
            if df is not None:
                # Convert DataFrame to JSON
                products_json = json.loads(df.to_json(orient='records'))
                return jsonify({'data': products_json,
                                'message': "Data fetched successfully",
                                'status': 'success'
                                })
            else:
                return jsonify({'message': 'Failed to fetch user data',
                                "status": "error"})

        except Exception as e:
            return jsonify({"status": "error",
                            "message": str(e)})