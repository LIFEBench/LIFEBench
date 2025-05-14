import argparse

from evaluate.evaluate_all_results import evaluate

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_dir",
        type=str,
        default="./result",
        required=False,
        help='Directory containing the data to be evaluated. Default: ./result'
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./evaluate_result",
        required=False,
        help='Directory to save the evaluation results. Default: ./evaluate_result'
    )
    args = parser.parse_args()

    # Run the evaluation process
    evaluate(args.data_dir, args.output_dir)
    print(f"Evaluation completed. Results have been saved to: {args.output_dir}")
