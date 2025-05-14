from openai import OpenAI

from exp.universe_api.BaseModel import BaseModel
from exp.universe_api.OpenAiBaseModel import OpenAiBaseModel


class OpenAiStreamModel(OpenAiBaseModel):
    def __init__(self, api_type, model_params, api_params):
        super().__init__(api_type, model_params, api_params)

    def _call_llm(self, prompt, args):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            **args
        )
        answer_content = ""
        reasoning_content = ""
        for chunk in response:
            delta = chunk.choices[0].delta
            if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
                reasoning_content += delta.reasoning_content
            if hasattr(delta, "content") and delta.content:
                answer_content += delta.content
        return {"response": answer_content, "thinking": reasoning_content}

    def clear(self):
        self.client = None
