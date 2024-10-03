import os
from typing import List

from TibWordGathering.utils import is_valid_data_point, save_json


def process_file(file_path: str):
    """
    Processes a single text file and returns a list of valid data points.
    Each data point is a dictionary with 'source', 'target', and 'filename' keys.

    Parameters:
    file_path (str): The path to the text file.

    Returns:
    tuple: A tuple containing two lists - valid data and invalid data.
    """
    valid_data: List[dict] = []
    invalid_data: List[dict] = []
    current_sentence: List[str] = []
    filename = os.path.basename(file_path)

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            words = line.split()

            for word in words:
                if word == "<utt>":
                    if current_sentence:
                        source = "".join(current_sentence)
                        target = " ".join(current_sentence)
                        data_point = {
                            "source": source,
                            "target": target,
                            "filename": filename,
                        }
                        if is_valid_data_point(data_point):
                            valid_data.append(data_point)
                        else:
                            invalid_data.append(data_point)
                        current_sentence = []
                elif word.startswith("p") and word[1:].isdigit():
                    # Found a page number within the text
                    if current_sentence:
                        # Save the current sentence before changing the page
                        source = "".join(current_sentence)
                        target = " ".join(current_sentence)
                        data_point = {
                            "source": source,
                            "target": target,
                            "filename": filename,
                        }
                        if is_valid_data_point(data_point):
                            valid_data.append(data_point)
                        else:
                            invalid_data.append(data_point)
                    current_sentence = []
                else:
                    current_sentence.append(word)

    # Handle any remaining sentence
    if current_sentence:
        source = "".join(current_sentence)
        target = " ".join(current_sentence)
        data_point = {"source": source, "target": target, "filename": filename}
        if is_valid_data_point(data_point):
            valid_data.append(data_point)
        else:
            invalid_data.append(data_point)

    return valid_data, invalid_data


def process_folder(folder_path: str, valid_output_file: str, invalid_output_file: str):
    """
    Processes all text files in the given folder and aggregates the results into two JSON files:
    one for valid data and one for invalid data.

    Parameters:
    folder_path (str): The path to the folder containing text files.
    valid_output_file (str): The file path where valid data will be saved.
    invalid_output_file (str): The file path where invalid data will be saved.
    """
    all_valid_data = []
    all_invalid_data = []

    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            for filename in os.listdir(os.path.join(root, dir)):
                if filename.endswith(".txt"):
                    file_path = os.path.join(root, dir, filename)
                    valid_data, invalid_data = process_file(file_path)
                    all_valid_data.extend(valid_data)
                    all_invalid_data.extend(invalid_data)

    # Save all valid data into one JSON file
    save_json(all_valid_data, valid_output_file)

    # Save all invalid data into another JSON file
    if all_invalid_data:
        save_json(all_invalid_data, invalid_output_file)


if __name__ == "__main__":
    folder_path = "data/input/SegPos"
    valid_output_file = "data/output/segpos_tib_word/segpos_tib_word_valid_data.json"
    invalid_output_file = (
        "data/output/segpos_tib_word/segpos_tib_word_invalid_data.json"
    )
    # Ensure the parent directories exist
    os.makedirs(os.path.dirname(valid_output_file), exist_ok=True)
    os.makedirs(os.path.dirname(invalid_output_file), exist_ok=True)
    process_folder(folder_path, valid_output_file, invalid_output_file)
