import os
from pathlib import Path

import conllu

from TibWordGathering.utils import is_valid_data_point, save_json


def process_conllu_file(file_path):
    valid_data = []
    invalid_data = []  # List to store invalid data
    current_data = {"source": "", "target": "", "filename": ""}

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

            # Add filename and append to the respective list
            current_data = {
                "source": source_text,
                "target": target_text,
                "filename": os.path.basename(file_path),
            }
            if is_valid_data_point(current_data):
                valid_data.append(current_data)
            else:
                invalid_data.append(current_data)  # Append invalid data
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            continue
    return valid_data, invalid_data  # Return both valid and invalid data


def process_conllu_folder(folder_path, valid_output_file, invalid_output_file):
    """
    Processes all CoNLL-U files in the given folder and saves the results to separate JSON files for valid and invalid data.

    Parameters:
    folder_path (str): The path to the folder containing CoNLL-U files.
    valid_output_file (str): The path to the output JSON file where valid data will be saved.
    invalid_output_file (str): The path to the output JSON file where invalid data will be saved.
    """  # noqa
    combined_valid_data = []
    combined_invalid_data = []

    # Process each CoNLL-U file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".conllu"):
            file_path = os.path.join(folder_path, filename)

            valid_data, invalid_data = process_conllu_file(file_path)
            combined_valid_data.extend(valid_data)
            combined_invalid_data.extend(invalid_data)

    # Save the valid data into one JSON file
    save_json(combined_valid_data, valid_output_file)

    # Save the invalid data into another JSON file
    save_json(combined_invalid_data, invalid_output_file)


if __name__ == "__main__":
    conllu_file_dir = Path("./data/input/Conllu")
    valid_output_file_path = Path(
        "./data/output/conllu_tib_words/conllu_valid_data.json"
    )
    invalid_output_file_path = Path(
        "./data/output/conllu_tib_words/conllu_invalid_data.json"
    )

    # Ensure the output directories exist
    valid_output_file_path.parent.mkdir(parents=True, exist_ok=True)
    invalid_output_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Process all .conllu files and save valid/invalid data to separate JSON files
    process_conllu_folder(
        conllu_file_dir, valid_output_file_path, invalid_output_file_path
    )
