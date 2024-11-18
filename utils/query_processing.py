import pandas as pd
import requests
import streamlit as st
from streamlit import cache_data

# Define the backend URL
BACKEND_URL = "http://localhost:5000"

# Cache the function to load data from backend to avoid reloading on each interaction
@cache_data
def load_data_from_backend(file, start_row=0, end_row=None):
    """
    Load data from the backend (CSV upload) and return the columns and preview data.
    """
    try:
        response = requests.post(f"{BACKEND_URL}/upload_csv", files={"file": file})
        
        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            columns = data["columns"]
            
            # Load the preview data and apply row range slicing
            preview_data = pd.DataFrame(data["preview"])
            if end_row is None or end_row > len(preview_data):
                end_row = len(preview_data)  # Default to the last row if end_row is not specified or out of bounds
            preview_data = preview_data.iloc[start_row:end_row]
            
            return columns, preview_data
        else:
            st.error(f"Failed to load data from backend: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        st.error(f"Error loading data from backend: {str(e)}")
        return None, None

def load_data_from_google_sheet(url, start_row=0, end_row=None):
    """
    Load data from Google Sheets via the backend service and return the columns and preview data.
    """
    try:
        response = requests.post(f"{BACKEND_URL}/connect_google_sheet", json={"sheet_url": url})
        
        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            columns = data["columns"]
            
            # Load the preview data and apply row range slicing
            preview_data = pd.DataFrame(data["preview"])
            if end_row is None or end_row > len(preview_data):
                end_row = len(preview_data)
            preview_data = preview_data.iloc[start_row:end_row]
            
            return columns, preview_data
        else:
            st.error(f"Failed to load data from Google Sheets: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        st.error(f"Error loading data from Google Sheets: {str(e)}")
        return None, None

def search_entities_via_backend(entities, prompt_template):
    """
    Perform a search for multiple entities via the backend.
    """
    payload = {
        "entities": entities,
        "prompt_template": prompt_template
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/search_entities", json=payload)
        
        # Check for successful response
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error in search_entities_via_backend: {response.status_code} - {response.text}")
            return {}
    except Exception as e:
        st.error(f"Error in search_entities_via_backend: {str(e)}")
        return {}

