import pandas as pd
from flask import jsonify

def process_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return {"columns": df.columns.tolist(), "preview": df.head(5).to_dict(orient="records")}, 200
    except Exception as e:
        return {"error": "Invalid CSV file."}, 400
