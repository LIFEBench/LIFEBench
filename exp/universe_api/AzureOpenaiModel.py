from openai import AzureOpenAI

from exp.universe_api.BaseModel import BaseModel


class AzureOpenaiModel(BaseModel):
    def __init__(self, api_type, model_params, api_params):
        super().__init__(api_type, model_params)
        self.client = AzureOpenAI(**api_params)

    def _call_llm(self, prompt, args):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            **args
        )
        return response.choices[0].message.content

    def clear(self):
        self.client = None
