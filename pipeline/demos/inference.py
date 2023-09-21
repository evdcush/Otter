import sys
import requests
import yaml

from .demo_models import TestOtter, TestOtterIdefics
from .demo_utils import get_image, print_colored

requests.packages.urllib3.disable_warnings()


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="otter", help="The model name.")
    parser.add_argument("--checkpoint", type=str, required=True, help="The path to the checkpoint.")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.model_name == "otter":
        model = TestOtter(checkpoint=args.checkpoint)
    elif args.model_name == "otter_idefics":
        model = TestOtterIdefics(checkpoint=args.checkpoint)

    while True:
        yaml_file = input("Enter the path to the yaml file: (or 'q' to quit): ")
        if yaml_file == "q":
            break
        with open(yaml_file, "r") as file:
            test_data_list = yaml.safe_load(file)

        log_json_path = yaml_file.replace(".yaml", "_log.json")
        log_json = {}
        for test_id, test_data in enumerate(test_data_list):
            image_path = test_data.get("image_path", "")
            question = test_data.get("question", "")

            image = get_image(image_path)
            no_image_flag = not bool(image_path)

            response = model.generate(prompt=question, image=image, no_image_flag=no_image_flag)

            # Print results to console
            print(f"image_path: {image_path}")
            print_colored(f"question: {question}", color_code="\033[92m")
            print_colored(f"answer: {response}", color_code="\033[94m")
            print("-" * 150)

            log_json.update(
                {
                    str(test_id).zfill(3): {
                        "image_path": image_path,
                        "question": question,
                        "answer": response,
                    }
                }
            )

        with open(log_json_path, "w") as file:
            yaml.dump(log_json, file, default_flow_style=False)


if __name__ == "__main__":
    main()