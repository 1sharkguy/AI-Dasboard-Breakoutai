
# AI Agent Dashboard

## Project Description
This AI Agent Dashboard is designed to help users extract specific information from web searches for entities listed in a dataset. Users can upload a CSV file or connect to a Google Sheet, specify a custom search query for each entity, and retrieve the results in a structured format. The AI agent uses a combination of web search and LLM (Language Learning Model) parsing to deliver the requested data efficiently. The dashboard provides a user-friendly interface to download, and update extracted information.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/1sharkguy/AI-Dasboard-Breakoutai.git
   cd AI-Dasboard-Breakoutai
   ```

2. **Install dependencies:**
   Install the required dependencies listed in `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory with your API keys and database configurations. Here’s an example `.env` setup:
   ```plaintext
   GOOGLE_SHEETS_API_KEY="your-google-sheets-api-key"
   SERPAPI_KEY="your-serpapi-key"
   POSTGRES_USER="postgres"
   POSTGRES_PASSWORD="your-postgres-password"
   POSTGRES_DB="postgres"
   POSTGRES_HOST="localhost"
   POSTGRES_PORT="5432"
   GROQ_API_KEY="your-groq-api-key"
   ```

4. **Run the application:**
   Start the Streamlit dashboard using the following command:
   ```bash
   streamlit run app.py
   ```

## Features

- **File Upload and Preview:** Upload CSV files, specify row ranges, and preview data.
- **Google Sheets Connection:** Connect to Google Sheets via URL, specify row ranges, and load data.
- **Custom Querying:** Define custom prompts to perform searches on uploaded data or Google Sheets data.
- **LLM-based Information Extraction:** Use LLM to extract structured information from search results.
- **Download and Save Data:** Export extracted information as a CSV file.

## Usage Guide

### 1. Selecting a View
- Choose between **File Upload** and **Google Sheets** modes to either upload a CSV file directly or connect to a Google Sheet.
- Use the buttons on the dashboard to toggle between these two modes.

### 2. Uploading Data (File Upload Mode)
- In "File Upload" mode, click "Browse" to upload one or more CSV files.
- After uploading, specify a range of rows for preview using the "Preview Start Row" and "Preview End Row" inputs.
- Click **"Update Preview with Selected Row Range"** to load and display the selected data rows.
- You can clear all uploaded files and reset the view by clicking **"Clear File Upload Data"**.

### 3. Connecting to Google Sheets (Google Sheets Mode)
- Enter the Google Sheets URL in the input field in "Google Sheets" mode.
- Specify a row range for preview by entering the start and end rows.
- Click **"Connect to Google Sheets"** to load data and display it within the specified range.
- You can reset the Google Sheets data view by clicking **"Clear Google Sheets Data"**.

### 4. Selecting the Main Column
- After previewing the data, select a column from the dropdown menu that contains the entities you want to query (e.g., names of people, companies, or products).
- For example, select a column containing company names if you want to search for information about specific companies.

### 5. Setting Up Search Queries
- Enter a custom prompt in the input field, using `{entity}` as a placeholder for the selected column's values.
- Example prompt: `"Find the email address of {entity}."`
- The placeholder `{entity}` will be replaced with each entity from the selected column during the search.

### 6. Running the Search (Web Search for Entities)
- Click **"Perform Web Search for Entities"** to initiate searches based on the entities and custom prompt.
- Results will be displayed in the dashboard under **Search Results** for each entity in a structured format, with links, titles, and snippets of the search results.

### 7. Extracting Information Using LLM (Optional)
- After viewing search results, enter a prompt to extract specific information from the results using an LLM.
- For example, you can use `"Extract the email address of {entity}"` to retrieve email addresses from search results.
- Click **"Extract Information with LLM"** to start the extraction process. Results will be displayed in the dashboard.

### 8. Downloading and Saving Data
- After extracting information, click **"Download Extracted Data"** to save the results as a CSV file.
- For Google Sheets users, you may optionally update the connected sheet with the retrieved information by following any custom integration steps provided in the code (if applicable).

---

## API Keys and Environment Variables

- **GOOGLE_SHEETS_API_KEY**: API key for accessing Google Sheets data.
- **SERPAPI_KEY**: API key for SerpAPI or any other web search API.
- **POSTGRES_USER**: PostgreSQL database username.
- **POSTGRES_PASSWORD**: PostgreSQL database password.
- **POSTGRES_DB**: PostgreSQL database name.
- **POSTGRES_HOST**: Database host (e.g., `localhost`).
- **POSTGRES_PORT**: Database port (default is `5432`).
- **GROQ_API_KEY**: API key for Groq or any other LLM service used in the project.

All sensitive information should be stored in the `.env` file to avoid hardcoding in the source code. Refer to the example `.env` file provided above for proper setup.

## Optional Features

- **Advanced Query Templates**: Supports multi-field extraction in a single prompt (e.g., "Get the email and address for {company}").
- **Google Sheets Output Integration**: Directly write back the extracted data to the connected Google Sheet.
- **Error Handling**: Enhanced error handling to manage failed API calls or incomplete LLM queries, with user notifications.

## Project Deliverables

1. **GitHub Repository**: A well-structured repository containing all the project files and this `README.md`.
2. **Loom Video**: A 2-minute walkthrough video demonstrating the key features and functionalities of the project.
3. https://www.loom.com/share/e1543798ed5c4a589fda2620ae625c31?sid=c473f941-3830-49a9-9188-96b23b6da021
4. **Dashboard**: A Streamlit dashboard providing the described functionalities.

For any further assistance, feel free to reach out.

