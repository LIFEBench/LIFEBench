from exp.universe_api.PipelineModel import PipelineModel


class LongWriterModel(PipelineModel):
    def __init__(self, api_type, model_params):
        super().__init__(api_type, model_params)
        self.model_name = model_params.get("model", None)

    def _call_llm(self, prompt, args: dict):
        args.pop("model", None)
        if "llama" in self.model_name:
            prompt = f"[INST]{prompt}[/INST]"
            inputs = self.tokenizer(prompt, truncation=False, return_tensors="pt").to(self.model.device)
            context_length = inputs.input_ids.shape[-1]
            output = self.model.generate(
                **inputs,
                **args
            )[0]
            response = self.tokenizer.decode(output[context_length:], skip_special_tokens=True)
        else:
            response, history = self.model.chat(self.tokenizer, prompt, history=[], **args)

        return response
