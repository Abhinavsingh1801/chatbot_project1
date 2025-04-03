from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Get API keys from .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        # Google Custom Search API request
        google_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
        google_res = requests.get(google_url, timeout=10)
        google_res.raise_for_status()  # Raise an error if API request fails
        google_data = google_res.json()

        results = [
            {"title": item["title"], "link": item["link"], "snippet": item["snippet"]}
            for item in google_data.get("items", [])
        ]
    except requests.exceptions.RequestException as e:
        results = []
        print(f"Google API Error: {e}")  # Debugging

    # OpenAI ChatGPT API request
    openai_headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    openai_payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": query}],
        "max_tokens": 100
    }

    try:
        openai_res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=openai_headers,
            json=openai_payload,
            timeout=10
        )
        openai_res.raise_for_status()
        openai_data = openai_res.json()
        chat_response = openai_data.get("choices", [{}])[0].get("message", {}).get("content", "No response from ChatGPT")
    except requests.exceptions.RequestException as e:
        chat_response = f"Error fetching ChatGPT response: {e}"

    return jsonify({"results": results, "chatGptResponse": chat_response})

# Run Flask app on port 5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)