import os
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/form-submission", methods=["POST"])
def handle_request():
    api_key = request.headers.get("x-api-key")
    if api_key != os.getenv("API_KEY"):
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json
        print("Received JSON Body:", data)
        return jsonify({"message": "JSON received successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Invalid JSON"}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use the PORT environment variable
    app.run(host="0.0.0.0", port=port)
