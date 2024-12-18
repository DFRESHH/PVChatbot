import openai
import os
from dotenv import load_dotenv  # Import dotenv to load API key from .env

# Load environment variables
load_dotenv()

# Set your API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Validate that the API key is loaded
if not openai.api_key:
    raise ValueError("Error: OPENAI_API_KEY is missing. Check your .env file.")

# Function to communicate with GPT-4
def chat_with_gpt4(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Specify GPT-4 here
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the assistant's reply
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Interactive Chat Loop
if __name__ == "__main__":
    print("Chat with GPT-4! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting. Goodbye!")
            break
        response = chat_with_gpt4(user_input)
        print(f"GPT-4: {response}")

