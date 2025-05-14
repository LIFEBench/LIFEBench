import torch
import random
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from exp.universe_api.BaseModel import BaseModel


class PipelineModel(BaseModel):
    def __init__(self, api_type, model_params):
        super().__init__(api_type, model_params)
        self.set_seed(10)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_params["model"],
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_params["model"],
            trust_remote_code=True
        )

    def set_seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    def _call_llm(self, prompt, args: dict):
        messages = [
            {"role": "user", "content": prompt},
        ]
        args.pop("model", None)
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **model_inputs,
            **args
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return response

    def clear(self):
        del self.model
        del self.tokenizer
        self.model = None
        self.tokenizer = None
        torch.cuda.empty_cache()
