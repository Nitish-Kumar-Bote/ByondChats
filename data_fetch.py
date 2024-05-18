# data_fetch.py

import requests


def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def identify_sources(data):
    citations = []
    for item in data['data']:
        response_text = item['response']
        sources = item['source']
        for source in sources:
            if source['context'] in response_text:
                citations.append({"id": source['id'], "link": source['link']})
    return citations
