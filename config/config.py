import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configurations for file uploads and other settings
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
MAX_CONTENT_LENGTH = 1024 * 1024 * 1024  # 1 GB

# Google Sheets API Key (loaded as JSON from .env)
GOOGLE_SHEETS_API_KEY = json.loads(os.getenv("GOOGLE_SHEETS_API_KEY"))

# SerpAPI key
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# PostgreSQL settings
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# PostgreSQL connection URI
DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Langchain Settings
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")  # Langchain API key
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")  # Default endpoint
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "default_project")  # Your Langchain project name

# Print the configuration to verify it's loaded correctly
print(f"Loaded Configurations:")
print(f"Upload Folder: {UPLOAD_FOLDER}")
print(f"Max Content Length: {MAX_CONTENT_LENGTH}")
print(f"PostgreSQL URI: {DATABASE_URI}")
print(f"Langchain Endpoint: {LANGCHAIN_ENDPOINT}")
print(f"Langchain Project: {LANGCHAIN_PROJECT}")

