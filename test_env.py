import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")

print("Current Directory:", os.getcwd())
print(".env File Exists:", os.path.isfile(".env"))
