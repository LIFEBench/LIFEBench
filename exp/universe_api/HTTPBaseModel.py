import requests
from openai import OpenAI

from exp.universe_api.BaseModel import BaseModel


class HTTPBaseModel(BaseModel):
    def __init__(self, api_type, model_params, api_params):
        super().__init__(api_type, model_params)
        self.api_key = api_params["api_key"]
        self.base_url = api_params["base_url"]

    def _call_llm(self, prompt, args):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        messages = [
            {"role": "user", "content": prompt}
        ]
        payload = {
            "messages": messages,
            **args
        }
        response = requests.post(self.base_url, headers=headers, json=payload, timeout=2000)
        response.raise_for_status()
        data = response.json()
        msg = data["choices"][0]["message"]
        if "reasoning_content" in msg:
            return {"response": msg["content"], "thinking": msg["reasoning_content"]}
        else:
            return msg["content"]

    def clear(self):
        pass
