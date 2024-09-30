import json
import os


def combine_json_files(file_paths, output_file):
    """_summary_

    Args:
        file_paths (_type_): _description_
        output_file (_type_): _description_
    """
    combined_data = []

    # Iterate through each file path
    for file_path in file_paths:
        if file_path.endswith(".json"):  # Check if the file is a JSON file
            # Open and read the JSON file
            with open(file_path, encoding="utf-8") as file:
                data = json.load(file)

                # Append data to the combined list
                combined_data.extend(data)

    # Save the combined data to the output file
    with open(output_file, "w", encoding="utf-8") as output:
        json.dump(combined_data, output, ensure_ascii=False, indent=2)

    print(f"Combined {len(combined_data)} records into {output_file}")


# Usage example:
file_paths = [
    "data/output/conllu_tib_words/conllu_valid_data.json",
    "data/output/segpos_ekangyur_eTengyur_tib_word/segpos_ekangyur_eTengyur_tib_word_valid_data.json",
    "data/output/segpos_tib_word/segpos_tib_word_valid_data.json",
    "data/output/evaluate_tib_word/evaluate_valid_data.json",
    "data/output/Manual-dataset/manual_data_valid_data.json"
    # Add as many file paths as you need
]

output_file = "data/output/combined_word_seg_data/combined_word_seg_data.json"  # noqa  # The file where combined data will be saved
output_dir = os.path.dirname(output_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory {output_dir}")
combine_json_files(file_paths, output_file)
