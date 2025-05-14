import torch
from exp.universe_api.PipelineModel import PipelineModel
from peft import PeftModel, PeftConfig


class SuriModel(PipelineModel):
    def __init__(self, api_type, model_params):
        super().__init__(api_type, model_params)
        config = PeftConfig.from_pretrained(model_params["finetuned_model"])
        self.pretrained_model = self.model
        self.model = PeftModel.from_pretrained(self.pretrained_model, model_params["finetuned_model"])
        self.model_params.pop("finetuned_model", None)

    def clear(self):
        del self.model
        del self.pretrained_model
        del self.tokenizer
        self.model = None
        self.tokenizer = None
        torch.cuda.empty_cache()
