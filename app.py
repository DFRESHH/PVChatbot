print("App is starting...")

import openai
import os
from flask import Flask, request, jsonify, render_template  # Added render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Store conversation history for each user
conversations = {}

@app.route("/")
def home():
    # Serve the chatbot interface
    return render_template("index.html")

# Chat endpoint (existing code)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Parse user input
        data = request.get_json()
        user_id = data.get("user_id")
        message = data.get("message")

        if not user_id or not message:
            return jsonify({"error": "Both 'user_id' and 'message' are required"}), 400

        # Retrieve conversation history or start a new one
        if user_id not in conversations:
            conversations[user_id] = [
                {"role": "system", "content": "You are an iempathetic and nquisitive assistant. Always ask follow-up questions to engage the user, such as 'What has you here today?' or 'What do you mean by that?'. If the user uses emotional words like 'frustrated', 'stressed', or 'angry', acknowledge their emotions by repeating those words in your response."}
            ]

        # Append the user's message to the conversation
        conversations[user_id].append({"role": "user", "content": message})

        # Generate a response using the OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if GPT-4 is unavailable
            messages=conversations[user_id]
        )

        # Extract the assistant's reply
        assistant_message = response["choices"][0]["message"]["content"]

        # Add the assistant's reply to the conversation history
        conversations[user_id].append({"role": "assistant", "content": assistant_message})

        return jsonify({"response": assistant_message})

    except Exception as e:
        return jsonify({"error": str(e)})

# Error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found. Check the URL and try again."}), 404

if __name__ == "__main__":
    print("App is starting...")
    port = int(os.getenv("PORT", 5000))  # Use PORT from environment or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)







