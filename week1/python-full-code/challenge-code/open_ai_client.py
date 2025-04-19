from openai import OpenAI
import requests
import json
from typing import Dict

class OpenAIClient:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def get_json_response(self, model: str, system_prompt: str, user_prompt: str) -> Dict:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        # Extract the content and parse it as JSON
        content = response.choices[0].message.content
        return json.loads(content)

    