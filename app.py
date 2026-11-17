
import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/", methods=["GET"])
def home():
    return "ChatGPT server is running!"

@app.route("/", methods=["POST"])
def alice():
    data = request.json or {}

    user_text = data.get("request", {}).get(
        "original_utterance", ""
    )

    if not user_text:
        user_text = "Привет!"

    try:
        result = client.responses.create(
            model="gpt-4.1-mini",
            input=user_text
        )

        answer = result.output_text[:1000]

    except Exception:
        answer = "Произошла ошибка. Попробуй ещё раз."

    return jsonify({
        "version": "1.0",
        "response": {
            "text": answer,
            "end_session": False
        }
    })
