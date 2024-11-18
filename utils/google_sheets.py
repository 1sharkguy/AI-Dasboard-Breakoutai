from flask import jsonify
import pandas as pd
import gspread
from google.oauth2 import service_account
from config.config import GOOGLE_SHEETS_API_KEY

def connect_google_sheet(sheet_url, start_row=0, end_row=None):
    try:
        # Define Google Sheets API scope
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        
        # Authenticate using Google Sheets API credentials
        credentials = service_account.Credentials.from_service_account_info(
            GOOGLE_SHEETS_API_KEY, scopes=scopes
        )
        client = gspread.authorize(credentials)
        
        # Access the first sheet by URL
        sheet = client.open_by_url(sheet_url).sheet1
        rows = sheet.get_all_values()
        
        # Convert sheet data into a DataFrame
        df = pd.DataFrame(rows[1:], columns=rows[0])  # Assuming the first row is the header
        
        # Apply row slicing
        if end_row is not None:
            df = df.iloc[start_row:end_row]
        else:
            df = df.iloc[start_row:]
        
        # Prepare JSON response
        response = {
            "columns": df.columns.tolist(),
            "preview": df.to_dict(orient="records")
        }
        return jsonify(response), 200

    except gspread.exceptions.SpreadsheetNotFound:
        return jsonify({"error": "Spreadsheet not found. Please check the URL and ensure the service account has access."}), 404
    except gspread.exceptions.APIError as e:
        return jsonify({"error": f"Google Sheets API error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500
