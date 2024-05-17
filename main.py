from difflib import SequenceMatcher

import requests


def fetch_data_from_api():
    base_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    data = []
    page = 1
    while True:
        response = requests.get(f"{base_url}?page={page}")
        if response.status_code != 200:
            break
        page_data = response.json()
        if not page_data:
            break
        data.extend(page_data)
        page += 1
    return data

def is_text_similar(text1, text2, threshold=0.5):
    return SequenceMatcher(None, text1, text2).ratio() > threshold

def identify_sources_for_response(response_text, sources):
    citations = []
    for source in sources:
        if is_text_similar(response_text, source["context"]):
            citations.append({"id": source["id"], "link": source.get("link", "")})
    return citations

def extract_citations(data):
    all_citations = []
    for item in data:
        response_text = item['response']
        sources = item['sources']
        citations = identify_sources_for_response(response_text, sources)
        all_citations.append(citations)
    return all_citations

def main():
    data = fetch_data_from_api()
    all_citations = extract_citations(data)
    print(all_citations)

if __name__ == "__main__":
    main()
