import openai
import os
from dotenv import load_dotenv  

# Load environment variables
load_dotenv()

# Set your API key and Assistant ID from .env
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

# Validate that both keys are loaded
if not openai.api_key:
    raise ValueError("Error: OPENAI_API_KEY is missing. Check your .env file.")
if not assistant_id:
    raise ValueError("Error: ASSISTANT_ID is missing. Check your .env file.")

# Function to communicate with MAI
def chat_with_mai(prompt):
    try:
        # Create a new thread for conversation
        thread = openai.beta.threads.create(
            assistant_id=assistant_id,
            messages=[{"role": "user", "content": prompt}]
        )

        # Get MAI's response
        response = thread["choices"][0]["message"]["content"]
        return response

    except Exception as e:
        return f"Error: {str(e)}"

# Interactive Chat Loop with MAI
if __name__ == "__main__":
    print("Chat with MAI! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting. Goodbye!")
            break
        response = chat_with_mai(user_input)
        print(f"MAI: {response}")
