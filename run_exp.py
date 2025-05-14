import os
import sys
import argparse
from exp.ModelType import ModelType
from exp.exp_request import exp_request


def parse_args():
    parser = argparse.ArgumentParser(description="Run main experiment with specified model and length types.")

    parser.add_argument(
        "--meta_data_path",
        type=str,
        default="./data/data.jsonl",
        required=False,
        help="Path to the meta data file. Default: ./data/data.jsonl"
    )

    parser.add_argument(
        "--output_file_dir",
        type=str,
        default="./result",
        required=False,
        help="Directory to save output files. Default: ./result"
    )

    parser.add_argument(
        "--model_type",
        type=str,
        required=False,
        default="GPT_4o_mini",
        choices=[
            "GPT_4o_mini",
            "GPT_4o",
            "o1_mini",
            "o3_mini",
            "Claude_37_sonnet",
            "Claude_37_sonnet_thinking",
            "Gemini_2_flash",
            "Gemini_2_flash_thinking",
            "Gemini_25_pro",
            "Doubao_15_pro",
            "Doubao_15_thinking_pro",
            "Deepseek_V3",
            "Deepseek_R1",
            "Llama31_8B",
            "Llama31_70B",
            "Qwen3_235B",
            "Qwen3_235B_Thinking",
            "Qwen3_32B",
            "Qwen3_32B_Thinking",
            "Qwen25_7B",
            "Qwen25_72B",
            "GLM4_9B",
            "Mistral_7B",
            "LongWriter_GLM4_9B",
            "LongWriter_Llama31_8B",
            "Suri"
        ],
        help=(
            "ModelType name, e.g., Qwen3_32B. "
            "Choices: GPT_4o_mini, GPT_4o, o1_mini, o3_mini, Claude_37_sonnet, "
            "Claude_37_sonnet_thinking, Gemini_2_flash, Gemini_2_flash_thinking, Gemini_25_pro, "
            "Doubao_15_pro, Doubao_15_thinking_pro, Deepseek_V3, Deepseek_R1, Llama31_8B, "
            "Llama31_70B, Qwen3_235B, Qwen3_235B_Thinking, Qwen3_32B, Qwen3_32B_Thinking, "
            "Qwen25_7B, Qwen25_72B, GLM4_9B, Mistral_7B, LongWriter_GLM4_9B, "
            "LongWriter_Llama31_8B, Suri. Default: GPT_4o_mini"
        )
    )
    parser.add_argument(
        "--length_constraints",
        type=int,
        nargs="+",
        required=False,
        default=[16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192],
        help="List of length constraints, Default: [16,32,64,128,256,512,1024,2048,4096,8192]"
    )

    parser.add_argument(
        "--control_methods",
        type=str,
        nargs="+",
        choices=["equal to", "at most", "at least"],
        default=["equal to"],
        required=False,
        help='List of control methods. Choices: "equal to", "at most", "at least". Default: ["equal to"]'
    )

    parser.add_argument(
        "--param_config_file",
        type=str,
        default="./exp/model_param_config.yaml",
        required=False,
        help='Path to the model parameter config file. Default: ./exp/model_param_config.yaml'
    )

    parser.add_argument(
        "--key_config_file",
        type=str,
        default="./exp/model_key_config.yaml",
        required=False,
        help='Path to the model key config file. Default: ./exp/model_key_config.yaml'
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        model_type = getattr(ModelType, args.model_type)
    except AttributeError:
        print(f"Invalid model_type: {args.model_type}. Available: {[m for m in ModelType.__members__]}")
        sys.exit(1)

    meta_data_path = args.meta_data_path
    output_file_dir = args.output_file_dir
    control_methods = args.control_methods
    length_constraints = args.length_constraints
    api_type = ModelType.get_api_type(model_type)
    output_file_dir = os.path.join(output_file_dir, api_type)
    print(f"Meta Data Path: \"{meta_data_path}\"")
    print(f"Evaluation Result are Saved in: \"{output_file_dir}\"")
    print(f"Model: {model_type}")
    print(f"Control Methods: {control_methods}")
    print(f"Length constraints: {length_constraints}")
    param_config_file = args.param_config_file
    key_config_file = args.key_config_file
    exp_request(meta_data_path, output_file_dir, control_methods, length_constraints, api_type, key_config_file,
                param_config_file,
                )


if __name__ == "__main__":
    main()
