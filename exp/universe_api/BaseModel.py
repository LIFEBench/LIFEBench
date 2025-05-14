import json
import os
import time
from abc import ABC, abstractmethod

from exp.cache import load_cache, save_cache, count_words


class BaseModel(ABC):

    def __init__(self, api_type, model_params):
        self.meta_data = None
        self.length_constraint = None
        self.control_method = None
        self.api_type = api_type
        self.model_params = model_params
        self.output_file = ""
        self.cache_file = ""

    def prepare_dir(self, output_file_dir, control_method, length_constraint):
        self.control_method = control_method
        self.length_constraint = length_constraint
        output_dir = os.path.join(output_file_dir, f"{self.control_method}")
        os.makedirs(output_dir, exist_ok=True)
        self.output_file = os.path.join(output_dir, f"{self.length_constraint}.jsonl")
        cache_dir = os.path.join(output_dir, "cache")
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_file = os.path.join(cache_dir, f"{self.length_constraint}_cache.json")

    def get_cache_data(self, meta_data):
        self.meta_data = meta_data
        cached_responses = load_cache(self.cache_file)
        existing_indices = set(cached_responses.keys())
        total_indices = set(range(len(self.meta_data)))
        remaining_indices = sorted(total_indices - existing_indices)
        if not remaining_indices:
            print("All prompts have been processed.")
            self._store_cache(cached_responses)
            return
        for idx in remaining_indices:
            max_retries = 3
            success = False

            for attempt in range(max_retries):
                try:
                    prompt = self.meta_data[idx]['prompt']
                    begin_time = time.time()
                    response = self._call_llm(prompt, self.model_params)
                    thinking = ""
                    if isinstance(response, dict):
                        thinking = response['thinking']
                        response = response['response']
                    # Calculate and store word count immediately
                    end_time = time.time()
                    cached_responses[idx] = {
                        "response": response,
                        "thinking": thinking,
                        "word_count": count_words(response),
                        "time": end_time - begin_time,
                        **self.meta_data[idx]
                    }
                    # Save updated cache immediately
                    save_cache(self.cache_file, cached_responses)
                    print(f"Index {idx} processed, cache updated.")
                    success = True
                    break  # Exit retry loop if successful
                except Exception as e:
                    error_msg = f"Error occurred while processing index {idx} (attempt {attempt + 1}/{max_retries}): {e}"
                    if attempt < max_retries - 1:
                        error_msg += ", retrying in 3 seconds..."
                        print(error_msg)
                        time.sleep(3)
                    else:
                        print(error_msg + ", giving up retry")
            if not success:
                print(f"Index {idx} failed after {max_retries} attempts, skipping.")
                continue  # Continue to next index
        self._store_cache(cached_responses)

    def _store_cache(self, cached_responses):
        with open(self.output_file, "w", encoding="utf-8") as f:  # Overwrite mode
            for idx in sorted(cached_responses.keys()):
                data = cached_responses[idx]
                # Remove prompt from cache structure directly
                data.pop("prompt", None)
                f.write(json.dumps({
                    "index": idx,
                    "control_method": self.control_method,
                    "length_constraint": self.length_constraint,
                    "api_type": self.api_type,
                    **data,
                }, ensure_ascii=False) + "\n")

    @abstractmethod
    def _call_llm(self, prompt, args):
        pass

    @abstractmethod
    def clear(self):
        pass
