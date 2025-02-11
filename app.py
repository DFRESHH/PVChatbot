ffrom flask import Flask, request, jsonify, render_template
import openai
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)  # The app object that Gunicorn needs

# Your routes go here
@app.route('/')
def home():
    return render_template("index.html")

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

app = Flask(__name__)

# Store conversation history
conversations = {}

# Load training data
training_data = None  # Default to None in case loading fails
training_data_path = "data/mai_training_data.json"  # Adjust the path as needed

try:
    with open(training_data_path, 'r') as file:
        training_data = json.load(file)
        print("Training data loaded successfully.")
except FileNotFoundError:
    print(f"Training data file not found: {training_data_path}")
except json.JSONDecodeError:
    print("Error decoding JSON in training data file.")
except Exception as e:
    print(f"Unexpected error loading training data: {e}")


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
            system_message = "You are Mai, your intuitive and persuasive sales assistant. Start every conversation by introducing yourself and asking what has you looking into this project, such as: 'Hi, I'm Mai! What has you looking into us today?'"

            # Inject training data only once
            if training_data:
                training_context = " ".join(
                    [entry['content'] for entry in training_data if entry['role'] == "assistant"]
                )
                system_message += f" Additional context: {training_context}"

            conversations[user_id] = [{"role": "system", "content": system_message}]

        # Append the user's message
        conversations[user_id].append({"role": "user", "content": message})

        # Limit conversation length to prevent token overload
        MAX_MESSAGES = 20
        if len(conversations[user_id]) > MAX_MESSAGES:
            conversations[user_id] = conversations[user_id][-MAX_MESSAGES:]

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

    except openai.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in request."}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route("/reset", methods=["POST"])
def reset():
    """Allows users to reset their conversation."""
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "'user_id' is required"}), 400

        if user_id in conversations:
            del conversations[user_id]

        return jsonify({"message": "Conversation reset successfully."})

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    # Use the PORT environment variable or default to 5000
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
