import json

import yaml

from exp.universe_api.AnthropicModel import AnthropicModel
from exp.universe_api.AzureOpenaiModel import AzureOpenaiModel
from exp.universe_api.GenAiModel import GenAiModel
from exp.universe_api.HTTPBaseModel import HTTPBaseModel
from exp.universe_api.OpenAiBaseModel import OpenAiBaseModel
from exp.universe_api.OpenAiStreamModel import OpenAiStreamModel
from exp.universe_api.PipelineModel import PipelineModel
from exp.universe_api.SuriModel import SuriModel
from exp.universe_api.LongWriterModel import LongWriterModel


def try_api_call(model, meta_data, output_file_dir, control_method, length_constraint):
    model.prepare_dir(output_file_dir, control_method, length_constraint)
    model.get_cache_data(meta_data)


def select_model(api_type, key_config_file, param_config_file):
    with open(param_config_file, 'r', encoding='utf-8') as file:
        model_params = yaml.safe_load(file).get(api_type, {})
    with open(key_config_file, 'r', encoding='utf-8') as file:
        api_params = yaml.safe_load(file).get(api_type, {})

    openai_base_api_type = ["gpt-4o-mini", "gpt-4o", "o1-mini", "deepseek-v3", "deepseek-r1", ]
    openai_stream_api_type = ["Qwen3-235B-A22B", "Qwen3-235B-A22B-Thinking", "Qwen3-32B", "Qwen3-32B-Thinking"]
    http_base_api_type = ["doubao-1.5-pro", "doubao-1.5-thinking-pro"]
    azure_base_api_type = ["o3-mini"]
    genai_base_api_type = ["gemini-2.0-flash", "gemini-2.0-flash-thinking", "gemini-2.5-pro"]
    anthropic_base_api_type = ["claude-3.7-sonnet", "claude-3.7-sonnet-thinking"]
    pipeline_base_api_type = ["Llama-3.1-8B-Instruct", "Llama-3.1-70B-Instruct", "Qwen2.5-7B-Instruct",
                              "Qwen2.5-72B-Instruct", "glm-4-9b",
                              "Mistral-7B-Instruct"]
    long_writer_api_type = ["LongWriter-glm4-9b", "LongWriter-llama3.1-8b"]
    suri_api_type = ["suri-i-orpo"]
    if api_type in openai_base_api_type:
        model = OpenAiBaseModel(api_type, model_params, api_params)
    elif api_type in openai_stream_api_type:
        model = OpenAiStreamModel(api_type, model_params, api_params)
    elif api_type in pipeline_base_api_type:
        model = PipelineModel(api_type, model_params)
    elif api_type in azure_base_api_type:
        model = AzureOpenaiModel(api_type, model_params, api_params)
    elif api_type in genai_base_api_type:
        model = GenAiModel(api_type, model_params, api_params)
    elif api_type in anthropic_base_api_type:
        model = AnthropicModel(api_type, model_params, api_params)
    elif api_type in http_base_api_type:
        model = HTTPBaseModel(api_type, model_params, api_params)
    elif api_type in long_writer_api_type:
        model = LongWriterModel(api_type, model_params)
    elif api_type in suri_api_type:
        model = SuriModel(api_type, model_params)
    else:
        raise Exception(f"No api type names: {api_type}")
    return model


def exp_request(meta_data_path, output_file_dir, control_methods, length_constraints, api_type, key_config_file,
                param_config_file):
    lang_adapt_dict = {
        'equal to': '等于',
        'at least': '至少有',
        'at most': '至多有'
    }
    model = select_model(api_type, key_config_file, param_config_file)
    params = model.model_params
    threshold = next(
        (params.get(k) for k in
         ["max_new_tokens", "max_completion_tokens", "max_output_tokens", "max_tokens", "max_length"]
         if params.get(k) is not None),
        0
    )
    for control_method in control_methods:
        for length_constraint in length_constraints:
            if int(length_constraint) > threshold:
                continue
            meta_data = []
            with open(meta_data_path, "r", encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    if "task" in data:
                        original_task = data["task"]
                        control_method_lang_adapt = control_method
                        if data['lang'] == 'cn':
                            control_method_lang_adapt = lang_adapt_dict[control_method]
                        modified_task = original_task.replace("{word_count_type}", control_method_lang_adapt)
                        modified_task = modified_task.replace("{word_count}", str(length_constraint))
                        meta_data.append({'prompt': modified_task,
                                          'type': data['type'],
                                          'category': data['category'],
                                          'lang': data['lang']}, )
                print(f"Processing control method: {control_method}, length constraint: {length_constraint}")
                try_api_call(model, meta_data, output_file_dir, control_method, length_constraint)
    model.clear()
