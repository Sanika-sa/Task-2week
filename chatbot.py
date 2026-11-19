import json
import random
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load intents dataset from JSON file
with open("intents.json", "r") as file:
    data = json.load(file)
    intents = data["intents"]

# In-memory session chat history log
chat_history = []

def preprocess_text(text):
    """Clean and normalize user text for matching."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', text).lower().strip()

def get_bot_response(user_input):
    """Match user input against intent patterns or return a fallback response."""
    cleaned_input = preprocess_text(user_input)
    
    if not cleaned_input:
        return "Please type a valid message."

    # Check for pattern matches across intents
    for intent in intents:
        for pattern in intent["patterns"]:
            if preprocess_text(pattern) in cleaned_input:
                return random.choice(intent["responses"])
                
    # Fallback response for unrecognized inputs
    return "I'm sorry, I didn't quite understand that. Could you please rephrase or ask something else?"

@app.route("/")
def index():
    """Render the main chat interface."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle incoming user messages and log session history."""
    user_message = request.json.get("message", "")
    bot_response = get_bot_response(user_message)
    
    # Log the interaction with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_history.append({
        "time": timestamp,
        "user": user_message,
        "bot": bot_response
    })
    
    return jsonify({"response": bot_response})

@app.route("/history", methods=["GET"])
def history():
    """Endpoint to view the full session chat history log."""
    return jsonify(chat_history)

if __name__ == "__main__":
    app.run(debug=True)