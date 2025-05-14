import os
import json


def get_model_list():
    return [
        "gpt-4o-mini",
        "gpt-4o",
        "o1-mini",
        "o3-mini",
        "claude-3.7-sonnet",
        "claude-3.7-sonnet-thinking",
        "gemini-2.0-flash",
        "gemini-2.0-flash-thinking",
        "gemini-2.5-pro",
        "doubao-1.5-pro",
        "doubao-1.5-thinking-pro",
        "deepseek-v3",
        "deepseek-r1",
        "Llama-3.1-8B-Instruct",
        "Llama-3.1-70B-Instruct",
        "Qwen2.5-7B-Instruct",
        "Qwen2.5-72B-Instruct",
        "Qwen3-32B",
        "Qwen3-32B-Thinking",
        "Qwen3-235B-A22B",
        "Qwen3-235B-A22B-Thinking",
        "glm-4-9b",
        "Mistral-7B-Instruct",
        "LongWriter-llama3.1-8b",
        "LongWriter-glm4-9b",
        "suri-i-orpo"
    ]


def get_model_name_mapping():
    return {
        "gpt-4o-mini": "GPT-4o mini",
        "gpt-4o": "GPT-4o",
        "o1-mini": "o1-mini",
        "o3-mini": "o3-mini",
        "claude-3.7-sonnet": "Claude-3.7-Sonnet",
        "claude-3.7-sonnet-thinking": "Claude-3.7-Sonnet-Thinking",
        "gemini-2.0-flash": "Gemini-2.0-Flash",
        "gemini-2.0-flash-thinking": "Gemini-2.0-Flash-Thinking",
        "gemini-2.5-pro": "Gemini-2.5-Pro",
        "doubao-1.5-pro": "Doubao-1.5-Pro",
        "doubao-1.5-thinking-pro" : "Doubao-1.5-Thinking-Pro",
        "deepseek-v3": "DeepSeek-V3",
        "deepseek-r1": "DeepSeek-R1",
        "Llama-3.1-8B-Instruct": "Llama-3.1-8B-Instruct",
        "Llama-3.1-70B-Instruct": "Llama-3.1-70B-Instruct",
        "Qwen2.5-7B-Instruct": "Qwen2.5-7B-Instruct",
        "Qwen2.5-72B-Instruct": "Qwen2.5-72B-Instruct",
        "Qwen3-32B": "Qwen3-32B",
        "Qwen3-32B-Thinking": "Qwen3-32B-Thinking",
        "Qwen3-235B-A22B": "Qwen3-235B-A22B",
        "Qwen3-235B-A22B-Thinking": "Qwen3-235B-A22B-Thinking",
        "glm-4-9b": "GLM-4-9B-Chat",
        "Mistral-7B-Instruct": "Mistral-7B-Instruct-v0.2",
        "LongWriter-llama3.1-8b": "LongWriter-Llama3.1-8B",
        "LongWriter-glm4-9b": "LongWriter-GLM4-9B",
        "suri-i-orpo": "Suri-I-ORPO"
    }


def collect_data(data_dir):
    control_method_order_list = [
        "equal to",
        "at most",
        "at least"
    ]
    collected_data = {}
    model_mapping = get_model_name_mapping()
    model_list = get_model_list()

    all_models = [m for m in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, m))]
    model_list = model_list or []
    all_models.sort(key=lambda x: model_list.index(x) if x in model_list else float('inf'))

    for model_name in all_models:
        mapped_name = model_mapping.get(model_name, model_name)
        model_path = os.path.join(data_dir, model_name)
        collected_data[mapped_name] = {}

        all_control_method = [lt for lt in os.listdir(model_path) if os.path.isdir(os.path.join(model_path, lt))]
        control_method_order_list = control_method_order_list or []
        all_control_method.sort(key=lambda x: control_method_order_list.index(x) if x in control_method_order_list else float('inf'))

        for control_method in all_control_method:
            length_path = os.path.join(model_path, control_method)
            collected_data[mapped_name][control_method] = {}

            numeric_files = []
            non_numeric_files = []

            for jsonl_file in os.listdir(length_path):
                if not jsonl_file.endswith(".jsonl"):
                    continue

                file_name = jsonl_file.replace(".jsonl", "")

                if file_name.isdigit():
                    numeric_files.append((int(file_name), jsonl_file))
                else:
                    non_numeric_files.append(jsonl_file)

            numeric_files.sort()
            sorted_files = [file for _, file in numeric_files] + non_numeric_files

            for jsonl_file in sorted_files:
                file_path = os.path.join(length_path, jsonl_file)
                data_entries = []
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            data_entries.append(json.loads(line.strip()))
                        except json.JSONDecodeError:
                            print(f"Warning: Skipping invalid JSON in {file_path}")
                jsonl_file = jsonl_file.replace(".jsonl", "")
                file_key = int(jsonl_file) if jsonl_file.isdigit() else jsonl_file
                collected_data[mapped_name][control_method][file_key] = data_entries

    return collected_data

