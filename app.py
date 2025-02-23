from flask import Flask, render_template, request, jsonify
import openai
import re

# Initialize Flask app
app = Flask(__name__)

# OpenAI API Key (Replace with your actual key)
client = openai.OpenAI(api_key="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")

# Custom responses database
custom_responses = {
    "hi":"Hi,this is Madhuri, how can I help you today?",
    "who made you": "I was created by Aryan Rai!",
    "who is aryan": "He is my creator.",
    "who is madhuri": "Madhuri is an AI language model developed by Aryan Rai. It’s designed to assist with answering questions, providing explanations, generating text, and helping with tasks like coding, troubleshooting, and learning new skills. You can think of it as a smart chatbot that can help with everything from IT support to casual conversations.",
    "your name": "Thanks for asking, My name is Madhuri. And what is yours?",
    "your full name": "Madhuri AI",
    "who": "Hi,This is Madhuri and I am an AI assistant developed by Aryan Rai.",
    "who are you": "My name is Madhuri and I am an AI assistant developed by Aryan Rai.",
    "what is your name": "I'm your custom chatbot; Madhuri, built just for you!",
    "listen madhuri":"I'm listening! What’s on your mind?",
    "madhuri":"Yes, tell me ! What’s on your mind?",
    "how is aryan":"He is very intelligent and sometimes silly person.",
    "how i s aryan":"He is very intelligent and sometimes silly person.",
    "how aryan is":"He is very intelligent and sometimes silly person."
}

# Function to normalize user input
def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"\bu\b", "you", text)  # Replace 'u' with 'you'
    text = re.sub(r"\br\b", "are", text)  # Replace 'r' with 'are'
    text = re.sub(r"[^a-z0-9\s+\-*/().]", "", text)   # Keep numbers, letters, spaces, and math symbols
    return text

# Function to get chatbot response
def chat_with_gpt(prompt):
    prompt = normalize_text(prompt)  # Normalize user input

    # Exact match check in custom responses
    if prompt in custom_responses:
        return custom_responses[prompt]

    # If no match, query OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Homepage route
@app.route("/")
def home():
    return render_template("index.html")

# API route for chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"response": "Invalid request"}), 400

    user_message = data["message"]
    bot_response = chat_with_gpt(user_message)
    return jsonify({"response": bot_response})

# Run Flask app on system's IP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
