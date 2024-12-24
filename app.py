from flask import Flask, request, jsonify, render_template
import openai
import os
import json  # Import for reading JSON files
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Store conversation history
conversations = {}

# Load training data
try:
    training_data_path = "data/mai_training_data.json"  # Path to your training data file
    with open(training_data_path, 'r') as file:
        training_data = json.load(file)
        print("Training data loaded successfully.")
except Exception as e:
    print(f"Error loading training data: {e}")
    training_data = None  # Fallback if the file fails to load

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Parse the incoming JSON request
        data = request.get_json()
        user_id = data.get("user_id")
        message = data.get("message")

        # Validate input
        if not user_id or not message:
            return jsonify({"error": "Both 'user_id' and 'message' are required"}), 400

        # Initialize conversation history if new user
        if user_id not in conversations:
            conversations[user_id] = [
                {
  "role": "system",
  "content": "You are Mai, your friendly and helpful assistant for ProjectVault. Start every conversation by introducing yourself and asking how you can help, such as: 'Hi, I'm Mai! How can I assist you with ProjectVault today?'"
}
            ]

        # Append the user's message
        conversations[user_id].append({"role": "user", "content": message})

        # Use training data if needed
        if training_data:
            # Example: Inject knowledge into system context dynamically
            training_context = " ".join([entry['content'] for entry in training_data if entry['role'] == "assistant"])
            conversations[user_id][0]['content'] += f" Here is additional context: {training_context}"

        # Generate a response using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversations[user_id]
        )

        # Extract the assistant's response
        assistant_message = response["choices"][0]["message"]["content"]

        # Append the assistant's response
        conversations[user_id].append({"role": "assistant", "content": assistant_message})

        return jsonify({"response": assistant_message})

    except KeyError:
        # Handle malformed JSON
        return jsonify({"error": "Malformed request. Please include 'user_id' and 'message'."}), 400

    except openai.error.OpenAIError as e:
        # Handle OpenAI API errors
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)





