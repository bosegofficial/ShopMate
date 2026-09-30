import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.6-flash"

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured in the .env file.")

client = genai.Client(api_key=API_KEY)

with open("chatbot_config.txt", "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    prompt = f"{SYSTEM_PROMPT}\n\nUser message:\n{message}"

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return jsonify({"reply": response.text or "I couldn't generate a response."})
    except Exception:
        return jsonify({
            "error": "Sorry, I couldn't connect to the AI service right now."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
