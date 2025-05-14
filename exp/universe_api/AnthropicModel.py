import anthropic
from anthropic import DefaultHttpxClient

from exp.universe_api.BaseModel import BaseModel


class AnthropicModel(BaseModel):
    def __init__(self, api_type, model_params, api_params):
        super().__init__(api_type, model_params)
        self.client = anthropic.Anthropic(
            **api_params,
        )
        self.model = model_params["model"]

    def _call_llm(self, prompt, args):
        args.pop("model", None)
        response = self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **args,
            timeout=2000
        )
        if len(response.content) > 1:
            return {"thinking": response.content[0].thinking, "response": response.content[1].text}
        else:
            return response.content[0].text

    def clear(self):
        self.client = None
