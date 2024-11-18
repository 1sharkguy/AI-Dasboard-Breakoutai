import streamlit as st
import pandas as pd
from utils.query_processing import (
    load_data_from_backend,
    load_data_from_google_sheet,
    search_entities_via_backend
)
import requests
import io

st.title("AI Dashboard")

# Initialize session state variables
if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = 0
if "uploaded_files_data" not in st.session_state:
    st.session_state.uploaded_files_data = {}
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None
if "file_upload_preview_data" not in st.session_state:
    st.session_state.file_upload_preview_data = pd.DataFrame()
if "search_results_file" not in st.session_state:
    st.session_state.search_results_file = {}
if "extraction_results_file" not in st.session_state:
    st.session_state.extraction_results_file = {}

if "sheet_columns" not in st.session_state:
    st.session_state.sheet_columns = []
if "sheet_preview_data" not in st.session_state:
    st.session_state.sheet_preview_data = pd.DataFrame()
if "search_results_sheet" not in st.session_state:
    st.session_state.search_results_sheet = {}
if "extraction_results_sheet" not in st.session_state:
    st.session_state.extraction_results_sheet = {}

# Function to reset session state for file uploads
def reset_file_upload_state():
    st.session_state.uploaded_files_data = {}
    st.session_state.selected_file = None
    st.session_state.file_uploader_key += 1
    st.session_state.file_upload_preview_data = pd.DataFrame()
    st.session_state.search_results_file = {}
    st.session_state.extraction_results_file = {}

# Function to reset session state for Google Sheets data
def reset_google_sheets_state():
    st.session_state.sheet_columns = []
    st.session_state.sheet_preview_data = pd.DataFrame()
    st.session_state.search_results_sheet = {}
    st.session_state.extraction_results_sheet = {}

# Initialize session state for view selection
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "file_upload"  # Default to file upload view

# Buttons to switch between file upload and Google Sheets URL views
col1, col2 = st.columns(2)
with col1:
    if st.button("File Upload"):
        st.session_state.view_mode = "file_upload"
with col2:
    if st.button("URL (Google Sheets)"):
        st.session_state.view_mode = "google_sheets"

# Section for File Upload
if st.session_state.view_mode == "file_upload":
    st.subheader("Upload CSV Files")

    # File upload input
    uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True, key=f"file_uploader_{st.session_state.file_uploader_key}")

    # Allow user to specify a range of rows for loading preview data
    st.write("### Select Range of Rows for Preview (File Upload)")
    preview_start = st.number_input("Preview Start Row", min_value=0, value=0, step=1)
    preview_end = st.number_input("Preview End Row", min_value=1, step=1)

    # Load each file's data and store it in session state
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.uploaded_files_data:
                try:
                    columns, preview_data = load_data_from_backend(uploaded_file, start_row=preview_start, end_row=preview_end)
                    if columns is not None and not preview_data.empty:
                        st.session_state.uploaded_files_data[uploaded_file.name] = {
                            "columns": columns,
                            "preview_data": preview_data[columns]
                        }
                        st.session_state.file_upload_preview_data = preview_data[columns]
                    else:
                        st.warning("No data available in the selected range. Please adjust the range.")
                except Exception as e:
                    st.error(f"An error occurred while loading '{uploaded_file.name}': {str(e)}")

    # Display file preview options if files are uploaded
    if st.session_state.uploaded_files_data:
        selected_file = st.selectbox("Select a file to preview", list(st.session_state.uploaded_files_data.keys()))
        st.session_state.selected_file = selected_file

        # Get the selected file's data
        file_data = st.session_state.uploaded_files_data[st.session_state.selected_file]
        columns = file_data["columns"]
        preview_data = file_data["preview_data"]

        # Display full columns within the selected row range in original order
        st.write(f"Preview of selected rows for '{st.session_state.selected_file}':", preview_data)

        # Allow user to specify a range of rows for the search
        st.write("### Select Range of Rows for Search")
        search_start = st.number_input("Search Start Row", min_value=0, max_value=len(preview_data) - 1, value=0, step=1)
        search_end = st.number_input("Search End Row", min_value=1, max_value=len(preview_data), value=len(preview_data), step=1)

        # Allow the user to select a column as the entity placeholder in the prompt
        placeholder_column = st.selectbox("Select a column for placeholder replacement in the prompt", columns)

        # Prompt template input for dynamic query generation
        st.write("### Dynamic Query Input with Prompt Template")
        prompt_template = st.text_input("Enter a custom prompt (use '{placeholder}' to insert entity value)", value="Get me the contact information for {placeholder}")
        st.session_state.prompt_template = prompt_template

        # Generate queries based on the selected column and search range
        if placeholder_column:
            entities = preview_data[placeholder_column].iloc[search_start:search_end].tolist()
            prompt_template = prompt_template.replace("{placeholder}", "{entity}")

            # Perform web search using SerpAPI and display results in the order of entities
            if st.button("Perform Web Search for Entities (File Upload)"):
                try:
                    with st.spinner("Searching..."):
                        search_results = search_entities_via_backend(entities, prompt_template)
                        st.session_state.search_results_file = search_results
                except Exception as e:
                    st.error(f"An error occurred during search: {str(e)}")

            # Display search results if available, ordered by entity list
            if "search_results_file" in st.session_state:
                st.write("### Search Results (File Upload)")
                for entity in entities:
                    results = st.session_state.search_results_file.get(str(entity), [])
                    st.write(f"Results for '{entity}':")
                    if results:
                        for result in results:
                            title = result.get("title", "No Title")
                            link = result.get("link", "No Link")
                            snippet = result.get("snippet", "No Snippet")
                            st.write(f"- **[{title}]({link})**: {snippet}")
                    else:
                        st.write("No results found.")
                    st.write("---")

        # Section for LLM-based information extraction for File Upload
        if "search_results_file" in st.session_state:
            st.write("### Extract Specific Information Using LLM for File Upload")
            user_prompt = st.text_input("Enter LLM prompt for file data", value="Extract the email address of {entity}")

            if st.button("Extract Information with LLM (File Upload)"):
                try:
                    with st.spinner("Processing with LLM..."):
                        response = requests.post(
                            "http://localhost:5000/extract_information",
                            json={
                                "entities": entities,
                                "search_results": st.session_state.search_results_file,
                                "prompt_template": user_prompt
                            }
                        )
                        if response.status_code == 200:
                            try:
                                st.session_state.extraction_results_file = response.json()
                            except requests.exceptions.JSONDecodeError:
                                st.error("Failed to decode JSON response from the server.")
                        else:
                            st.error(f"Request failed with status code {response.status_code}: {response.text}")
                except requests.RequestException as e:
                    st.error(f"An error occurred during the LLM extraction: {str(e)}")

            # Display extracted data for file upload
            if "extraction_results_file" in st.session_state:
                st.write("### Extracted Information (File Upload)")
                for entity, info in st.session_state.extraction_results_file.items():
                    st.write(f"{entity}: {info}")

                # Download button for extracted data as CSV
                extracted_data_file = pd.DataFrame.from_dict(st.session_state.extraction_results_file, orient='index', columns=["Extracted Info"])
                csv_file = extracted_data_file.to_csv(index=True)
                st.download_button("Download Extracted Data (File Upload)", data=csv_file, file_name="extracted_data_file.csv", mime="text/csv")
                    
    # Clear File Upload Data
    if st.button("Clear File Upload Data"):
        reset_file_upload_state()

# Section for Google Sheets URL connection
elif st.session_state.view_mode == "google_sheets":
    st.subheader("Connect to Google Sheets")

    # Google Sheets URL input
    sheet_url = st.text_input("Enter Google Sheet URL")

    # Allow user to specify a range of rows for loading preview data
    st.write("### Select Range of Rows for Preview (Google Sheets)")
    preview_start = st.number_input("Preview Start Row (Google Sheets)", min_value=0, value=0, step=1)
    preview_end = st.number_input("Preview End Row (Google Sheets)", min_value=1, step=1)

    if st.button("Connect to Google Sheets"):
        try:
            columns, preview_data = load_data_from_google_sheet(sheet_url, start_row=preview_start, end_row=preview_end)
            if columns is not None and preview_data is not None:
                st.session_state.sheet_columns = columns
                st.session_state.sheet_preview_data = preview_data[columns]
            else:
                st.warning("No data available in the selected range. Please adjust the range.")
        except Exception as e:
            st.error(f"An error occurred while loading data from Google Sheets: {str(e)}")

    # Display preview if data is loaded from Google Sheets
    if st.session_state.sheet_columns:
        st.write("Preview of selected rows (Google Sheets):", st.session_state.sheet_preview_data)

        # Allow user to specify a range of rows for search
        st.write("### Select Range of Rows for Search (Google Sheets)")
        search_start = st.number_input("Search Start Row (Google Sheets)", min_value=0, max_value=len(st.session_state.sheet_preview_data) - 1, value=0, step=1)
        search_end = st.number_input("Search End Row (Google Sheets)", min_value=1, max_value=len(st.session_state.sheet_preview_data), value=len(st.session_state.sheet_preview_data), step=1)

        # Select placeholder column
        placeholder_column = st.selectbox("Select a column for placeholder replacement in the prompt (Google Sheets)", st.session_state.sheet_columns)

        # Prompt template input
        st.write("### Dynamic Query Input with Prompt Template (Google Sheets)")
        prompt_template = st.text_input("Enter a custom prompt (use '{placeholder}' to insert entity value)", value="Get me the contact information for {placeholder}")
        st.session_state.prompt_template = prompt_template

        # Generate and perform search
        if placeholder_column:
            entities = st.session_state.sheet_preview_data[placeholder_column].iloc[search_start:search_end].tolist()
            prompt_template = prompt_template.replace("{placeholder}", "{entity}")

            if st.button("Perform Web Search for Entities (Google Sheets)"):
                try:
                    with st.spinner("Searching..."):
                        search_results = search_entities_via_backend(entities, prompt_template)
                        st.session_state.search_results_sheet = search_results
                except Exception as e:
                    st.error(f"An error occurred during search: {str(e)}")

            # Display search results in the order of the selected entities
            if "search_results_sheet" in st.session_state:
                st.write("### Search Results (Google Sheets)")
                for entity in entities:
                    results = st.session_state.search_results_sheet.get(str(entity), [])
                    st.write(f"Results for '{entity}':")
                    if results:
                        for result in results:
                            title = result.get("title", "No Title")
                            link = result.get("link", "No Link")
                            snippet = result.get("snippet", "No Snippet")
                            st.write(f"- **[{title}]({link})**: {snippet}")
                    else:
                        st.write("No results found.")
                    st.write("---")

        # Section for LLM-based information extraction for Google Sheets
        if "search_results_sheet" in st.session_state:
            st.write("### Extract Specific Information Using LLM for Google Sheets")
            user_prompt = st.text_input("Enter LLM prompt for Google Sheets data", value="Extract the email address of {entity}")

            if st.button("Extract Information with LLM (Google Sheets)"):
                try:
                    with st.spinner("Processing with LLM..."):
                        response = requests.post(
                            "http://localhost:5000/extract_information",
                            json={
                                "entities": entities,
                                "search_results": st.session_state.search_results_sheet,
                                "prompt_template": user_prompt
                            }
                        )
                        if response.status_code == 200:
                            try:
                                st.session_state.extraction_results_sheet = response.json()
                            except requests.exceptions.JSONDecodeError:
                                st.error("Failed to decode JSON response from the server.")
                        else:
                            st.error(f"Request failed with status code {response.status_code}: {response.text}")
                except requests.RequestException as e:
                    st.error(f"An error occurred during the LLM extraction: {str(e)}")

            # Display extracted data for Google Sheets
            if "extraction_results_sheet" in st.session_state:
                st.write("### Extracted Information (Google Sheets)")
                for entity, info in st.session_state.extraction_results_sheet.items():
                    st.write(f"{entity}: {info}")

                # Download button for extracted data as CSV
                extracted_data_sheet = pd.DataFrame.from_dict(st.session_state.extraction_results_sheet, orient='index', columns=["Extracted Info"])
                csv_sheet = extracted_data_sheet.to_csv(index=True)
                st.download_button("Download Extracted Data (Google Sheets)", data=csv_sheet, file_name="extracted_data_sheet.csv", mime="text/csv")

    # Clear Google Sheets Data
    if st.button("Clear Google Sheets Data"):
        reset_google_sheets_state()
