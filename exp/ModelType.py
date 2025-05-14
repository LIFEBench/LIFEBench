from enum import Enum, auto


class ModelType(Enum):
    GPT_4o_mini = auto()
    GPT_4o = auto()
    o1_mini = auto()
    o3_mini = auto()
    Claude_37_sonnet = auto()
    Claude_37_sonnet_thinking = auto()
    Gemini_2_flash = auto()
    Gemini_2_flash_thinking = auto()
    Gemini_25_pro = auto()
    Doubao_15_pro = auto()
    Doubao_15_thinking_pro = auto()
    Deepseek_V3 = auto()
    Deepseek_R1 = auto()
    Llama31_8B = auto()
    Llama31_70B = auto()
    Qwen3_235B = auto()
    Qwen3_235B_Thinking = auto()
    Qwen3_32B = auto()
    Qwen3_32B_Thinking = auto()
    Qwen25_7B = auto()
    Qwen25_72B = auto()
    GLM4_9B = auto()
    Mistral_7B = auto()
    LongWriter_GLM4_9B = auto()
    LongWriter_Llama31_8B = auto()
    Suri = auto()

    @staticmethod
    def get_api_type(model_type):
        api_type_dict = {
            ModelType.GPT_4o_mini: "gpt-4o-mini",
            ModelType.GPT_4o: "gpt-4o",
            ModelType.o1_mini: "o1-mini",
            ModelType.o3_mini: "o3-mini",
            ModelType.Claude_37_sonnet: "claude-3.7-sonnet",
            ModelType.Claude_37_sonnet_thinking: "claude-3.7-sonnet-thinking",
            ModelType.Gemini_2_flash: "gemini-2.0-flash",
            ModelType.Gemini_2_flash_thinking: "gemini-2.0-flash-thinking",
            ModelType.Gemini_25_pro: "gemini-2.5-pro",
            ModelType.Doubao_15_pro: "doubao-1.5-pro",
            ModelType.Doubao_15_thinking_pro: "doubao-1.5-thinking-pro",
            ModelType.Deepseek_V3: "deepseek-v3",
            ModelType.Deepseek_R1: "deepseek-r1",
            ModelType.Llama31_8B: "Llama-3.1-8B-Instruct",
            ModelType.Llama31_70B: "Llama-3.1-70B-Instruct",
            ModelType.Qwen3_235B: "Qwen3-235B-A22B",
            ModelType.Qwen3_235B_Thinking: "Qwen3-235B-A22B-Thinking",
            ModelType.Qwen3_32B: "Qwen3-32B",
            ModelType.Qwen3_32B_Thinking: "Qwen3-32B-Thinking",
            ModelType.Qwen25_7B: "Qwen2.5-7B-Instruct",
            ModelType.Qwen25_72B: "Qwen2.5-72B-Instruct",
            ModelType.GLM4_9B: "glm-4-9b",
            ModelType.Mistral_7B: "Mistral-7B-Instruct",
            ModelType.LongWriter_GLM4_9B: "LongWriter-glm4-9b",
            ModelType.LongWriter_Llama31_8B: "LongWriter-llama3.1-8b",
            ModelType.Suri: "suri-i-orpo"
        }
        return api_type_dict[model_type]
