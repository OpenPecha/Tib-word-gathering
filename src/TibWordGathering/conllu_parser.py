import os
from pathlib import Path

import conllu

from TibWordGathering.utils import is_valid_data_point, save_json


def process_conllu_file(file_path):
    valid_data = []
    invalid_data = []  # List to store invalid data
    current_data = {"source": "", "target": ""}

    # Open and read the conllu file
    with open(file_path, encoding="utf-8") as file:
        # Parse the file using conllu library
        sentences = conllu.parse(file.read(), fields=["id", "form"])

    # Extract the source text from the metadata
    for sentence in sentences:
        # Get the source from the metadata (e.g., # text = ...)
        try:
            target_text = ""
            if "text" in sentence.metadata:
                source_text = sentence.metadata["text"]

            # Extract the target text from the first column (the token)
            for token in sentence:
                target_text += token.get("form", "") + " "
            target_text = target_text.strip()
            current_data = {"source": source_text, "target": target_text}
            if is_valid_data_point(current_data):
                valid_data.append(current_data)
            else:
                invalid_data.append(current_data)  # Append invalid data
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            continue
    return valid_data, invalid_data  # Return both valid and invalid data


def process_conllu_folder(folder_path, output_folder):
    """
    Processes all CoNLL-U files in the given folder and saves the results to separate JSON files.

    Parameters:
    folder_path (str): The path to the folder containing CoNLL-U files.
    output_folder (str): The path to the folder where the output JSON files will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith(".conllu"):
            file_path = os.path.join(folder_path, filename)
            invalid_output_folder = output_folder / "invalid_data_json"
            invalid_output_folder.mkdir(parents=True, exist_ok=True)
            valid_output_folder = output_folder / "valid_data_json"
            valid_output_folder.mkdir(parents=True, exist_ok=True)

            valid_data, invalid = process_conllu_file(file_path)
            if invalid:
                output_file_invalid_data_path = os.path.join(
                    invalid_output_folder, filename.replace(".conllu", ".json")
                )
                save_json(invalid, output_file_invalid_data_path)

            output_file_valid_data_path = os.path.join(
                valid_output_folder, filename.replace(".conllu", ".json")
            )
            save_json(valid_data, output_file_valid_data_path)


if __name__ == "__main__":
    conllu_file_dir = Path("./data/input/Conllu")
    output_file_dir = Path("./data/output/conllu_json")
    output_file_dir.mkdir(parents=True, exist_ok=True)
    process_conllu_folder(conllu_file_dir, output_file_dir)
