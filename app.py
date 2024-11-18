import os
import pandas as pd
import gspread
from google.oauth2 import service_account
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename
from utils.file_processing import process_csv
from utils.google_sheets import connect_google_sheet
from utils.database import UploadedData, SessionLocal
from utils.search_api import search_entities
from utils.groq_api import extract_information_with_groq  # Import the new function
from config.config import UPLOAD_FOLDER, GOOGLE_SHEETS_API_KEY

from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load SERPAPI_KEY and Google Sheets API key from environment variables
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not SERPAPI_KEY:
    raise ValueError("SERPAPI_KEY environment variable is not set.")

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to handle CSV file upload and store metadata in PostgreSQL
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files['file']
    start_row = int(request.form.get('start_row', 0))
    end_row = request.form.get('end_row', None)

    df = pd.read_csv(file)

    # Handle row slicing
    if end_row is not None:
        end_row = int(end_row)
        df = df.iloc[start_row:end_row]
    else:
        df = df.iloc[start_row:]

    columns = df.columns.tolist()
    preview_data = df.head(5).to_dict(orient="records")
    return jsonify({"columns": columns, "preview": preview_data}), 200

# Google Sheets processing endpoint with row range support
@app.route('/connect_google_sheet', methods=['POST'])
def google_sheet():
    data = request.get_json()
    sheet_url = data.get('sheet_url')
    start_row = int(data.get('start_row', 0))
    end_row = data.get('end_row', None)

    if not sheet_url:
        return jsonify({"error": "Sheet URL missing."}), 400

    try:
        # Set up Google Sheets API credentials
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = service_account.Credentials.from_service_account_info(
            GOOGLE_SHEETS_API_KEY, scopes=scopes
        )
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(sheet_url).sheet1
        rows = sheet.get_all_values()
        df = pd.DataFrame(rows[1:], columns=rows[0])

        # Handle row slicing
        if end_row is not None:
            end_row = int(end_row)
            df = df.iloc[start_row:end_row]
        else:
            df = df.iloc[start_row:]

        columns = df.columns.tolist()
        preview_data = df.to_dict(orient="records")
        return jsonify({"columns": columns, "preview": preview_data}), 200

    except gspread.exceptions.SpreadsheetNotFound:
        return jsonify({"error": "Spreadsheet not found. Check URL and access."}), 404
    except gspread.exceptions.APIError as e:
        return jsonify({"error": f"Google Sheets API error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

# Web search for entities endpoint
@app.route('/search_entities', methods=['POST'])
def search_entities_endpoint():
    """
    Endpoint to perform web search for a list of entities using SerpAPI.
    Expects JSON payload with 'entities' and 'prompt_template'.
    """
    data = request.get_json()
    
    # Validate the payload
    if 'entities' not in data or 'prompt_template' not in data:
        return jsonify({"error": "Invalid payload. 'entities' and 'prompt_template' are required."}), 400

    entities = data['entities']
    prompt_template = data['prompt_template']
    
    # Perform search for each entity
    results = search_entities(entities, prompt_template, SERPAPI_KEY)
    
    return jsonify(results), 200

@app.route('/extract_information', methods=['POST'])
def extract_information():
    """
    Endpoint to send search results to the LLM (Groq) for information extraction.
    Expects JSON payload with 'entities', 'search_results', and 'prompt_template'.
    """
    data = request.get_json()

    # Validate the payload
    if 'entities' not in data or 'search_results' not in data or 'prompt_template' not in data:
        return jsonify({"error": "Invalid payload. 'entities', 'search_results', and 'prompt_template' are required."}), 400

    entities = data['entities']
    search_results = data['search_results']
    prompt_template = data['prompt_template']

    # Prepare extraction results
    extraction_results = {}

    for entity in entities:
        # Ensure entity is a string for proper prompt replacement
        entity_str = str(entity)
        entity_search_results = search_results.get(entity_str, [])

        # Replace {entity} placeholder in the prompt with the current entity's name
        prompt = prompt_template.replace("{entity}", entity_str)

        # Prepare search result context (assuming "snippet" is available)
        context = "\n".join(result.get("snippet", "") for result in entity_search_results)

        # Replace {context} placeholder in the prompt with the actual context
        prompt = prompt.replace("{context}", context)

        # Send to Groq API for processing
        try:
            extraction = extract_information_with_groq(prompt, entity_search_results)
            if "error" not in extraction:
                extraction_results[entity_str] = extraction.get("extracted_info", "No data found")
            else:
                extraction_results[entity_str] = f"Error: {extraction['error']}"
        except Exception as e:
            extraction_results[entity_str] = f"Error: {str(e)}"

    return jsonify(extraction_results), 200


if __name__ == '__main__':
    app.run(debug=True)
