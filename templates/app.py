import openai
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Define the Assistant ID
ASSISTANT_ID = "asst_5UHs8QhVNU2VX2Zns6NeHcpD"  # Replace with your actual ID

# Store threads for each user
threads = {}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Parse user input
        data = request.get_json()
        user_id = data.get("user_id")
        message = data.get("message")

        # Create a thread if it doesn't already exist
        if user_id not in threads:
            thread = openai.beta.threads.create()
            threads[user_id] = thread.id

        thread_id = threads[user_id]

        # Add the user's message to the thread
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )

        # Run the assistant
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )

        # Poll for the assistant's response
        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            print(f"Run Status: {run_status.status}")  # Debugging line
            if run_status.status in ["completed", "failed"]:
                break

        # Retrieve all messages in the thread
        messages = openai.beta.threads.messages.list(thread_id=thread_id)

        # Debug: Print all messages
        print("Messages in thread:")
        for msg in messages.data:
            print(f"{msg.role}: {msg.content[0].text.value}")

        # Get the assistant's response
        assistant_response = None
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                assistant_response = msg.content[0].text.value
                break

        if not assistant_response:
            assistant_response = "Sorry, I couldn't generate a response."

        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)


