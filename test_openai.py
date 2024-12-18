import openai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Test creating an assistant
try:
    assistant = openai.beta.assistants.create(
        name="Test Assistant",
        instructions="You are a helpful assistant.",
        model="gpt-4"
    )
    print("Assistant Created Successfully!")
    print("Assistant ID:", assistant.id)
except Exception as e:
    print(f"Error: {e}")
