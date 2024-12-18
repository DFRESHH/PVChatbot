import openai
import os
from dotenv import load_dotenv

# Step 1: Load API key from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 2: Create an Assistant
assistant = openai.beta.assistants.create(
    name="Customer Support Bot",
    instructions="You are a helpful assistant that provides support to customers about products, orders, and FAQs.",
    tools=[],  # No tools for now; we’ll add them later if needed
    model="gpt-4"  # You can use "gpt-3.5-turbo" if needed
)

# Step 3: Print the Assistant ID
print("Assistant created successfully!")
print("Assistant ID:", assistant.id)
