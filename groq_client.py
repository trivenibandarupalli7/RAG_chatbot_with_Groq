import os
import requests

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/v1"

    def chat(self, model, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": messages
        }
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        return response.json()["choices"][0]["message"]["content"]