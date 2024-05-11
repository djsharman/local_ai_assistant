import requests

def get_llama_response(prompt, context):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3-8b",
        "prompt": prompt,
        "context": context
    }
    response = requests.post(url, json=data)
    return response.json()['text']