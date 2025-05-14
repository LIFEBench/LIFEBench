from google import genai

from exp.universe_api.BaseModel import BaseModel
from google.genai import types


class GenAiModel(BaseModel):
    def __init__(self, api_type, model_params, api_params):
        super().__init__(api_type, model_params)
        self.client = genai.Client(**api_params)
        self.model = model_params["model"]

    def _call_llm(self, prompt, args):
        args.pop("model", None)
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                **args
            )
        )
        return response.text

    def clear(self):
        self.client = None
