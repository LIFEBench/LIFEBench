import json
import os
import re


def count_words(text):
    text = str(text)

    text = re.sub(r'\s+', ' ', text).strip()

    chinese_characters = re.findall(r'[\u4e00-\u9fff]', text)
    chinese_char_count = len(chinese_characters)

    english_words = re.findall(r'\b[a-zA-Z0-9\'-]+\b', text)
    english_word_count = len(english_words)

    # 统计总字数
    total_count = chinese_char_count + english_word_count

    return total_count


def load_cache(cache_file):
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    return {}


def save_cache(cache_file, responses):
    cache_data = {str(k): v for k, v in responses.items()}
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
