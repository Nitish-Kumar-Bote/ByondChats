from flask import Flask, jsonify, render_template
import requests
from difflib import SequenceMatcher

app = Flask(__name__)

def fetch_data_from_api():
    base_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    data = []
    for page in range(1, 14):  # Loop through pages 1 to 13
        response = requests.get(f"{base_url}?page={page}")
        if response.status_code != 200:
            print(f"Failed to fetch data from API: {response.status_code}")
            break
        try:
            page_data = response.json()
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            break
        if not page_data.get('data') or not page_data['data'].get('data'):
            break
        data.extend(page_data['data']['data'])
    return data

def is_text_similar(text1, text2, threshold=0.5):
    return SequenceMatcher(None, text1, text2).ratio() > threshold

def identify_sources_for_response(response_text, sources):
    citations = []
    for source in sources:
        if isinstance(response_text, str) and isinstance(source["context"], str):
            if is_text_similar(response_text.lower(), source["context"].lower()):
                citations.append({"id": source["id"], "link": source.get("link", "")})
    return citations
g
def extract_citations(data):
    all_citations = []
    for item in data:
        if isinstance(item, dict) and 'response' in item and 'source' in item:
            response_text = item['response']
            sources = item['source']
            citations = identify_sources_for_response(response_text, sources)
            all_citations.append(citations)
        else:
            print("Unexpected item format:", item)
    return all_citations

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/citations', methods=['GET'])
def get_citations():
    data = fetch_data_from_api()
    if data:
        all_citations = extract_citations(data)
        return jsonify(all_citations)
    else:
        return jsonify({"error": "No data fetched from API"}), 500

if __name__ == "__main__":
    app.run(debug=True)
