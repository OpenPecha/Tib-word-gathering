import os
from typing import List

from TibWordGathering.utils import is_valid_data_point, save_json


def process_file(file_path: str):
    """
    Processes a single text file and returns a list of data.
    Each data is a dictionary with 'source', 'target', and 'filename' as keys.
    The 'source' key contains the original sentence text, and the 'target' key contains the tokenized words.

    Parameters:
    file_path (str): The path to the text file.

    Returns:
    list: A list of valid data and a list of invalid data.
    """
    data: List[dict] = []
    invalid_data: List[dict] = []
    current_sentence: List[str] = []

    with open(file_path, encoding="utf-8") as file:
        filename = os.path.basename(file_path)
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
                            data.append(data_point)
                        else:
                            invalid_data.append(data_point)
                        current_sentence = []
                elif word.startswith("p") and word[1:].isdigit():
                    if current_sentence:
                        source = "".join(current_sentence)
                        target = " ".join(current_sentence)
                        data_point = {
                            "source": source,
                            "target": target,
                            "filename": filename,
                        }
                        if is_valid_data_point(data_point):
                            data.append(data_point)
                        else:
                            invalid_data.append(data_point)
                    current_sentence = []
                elif word.startswith("ln") and word[2:].isdigit():
                    continue
                else:
                    current_sentence.append(word)

    if current_sentence:
        source = "".join(current_sentence)
        target = " ".join(current_sentence)
        data_point = {"source": source, "target": target, "filename": filename}
        if is_valid_data_point(data_point):
            data.append(data_point)
        else:
            invalid_data.append(data_point)

    return data, invalid_data


def process_folder(folder_path: str, valid_output_file: str, invalid_output_file: str):
    """
    Processes all text files in the given folder and saves all valid data to one JSON file and all invalid data to another.

    Parameters:
    folder_path (str): The path to the folder containing text files.
    valid_output_file (str): Path to save the valid data JSON file.
    invalid_output_file (str): Path to save the invalid data JSON file.
    """  # noqa
    all_valid_data = []
    all_invalid_data = []

    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            for filename in os.listdir(os.path.join(root, dir)):
                if filename.endswith(".txt"):
                    file_path = os.path.join(root, dir, filename)
                    data, invalid_data = process_file(file_path)
                    all_valid_data.extend(data)
                    all_invalid_data.extend(invalid_data)

    # Save all valid data into one JSON file
    save_json(all_valid_data, valid_output_file)

    # Save all invalid data into another JSON file
    if all_invalid_data:
        save_json(all_invalid_data, invalid_output_file)


if __name__ == "__main__":
    folder_path = "data/input/SegPos-eKangyur-eTengyur"
    valid_output_file = "data/output/segpos_ekangyur_eTengyur_tib_word/segpos_ekangyur_eTengyur_tib_word_valid_data.json"  # noqa
    invalid_output_file = "data/output/segpos_ekangyur_eTengyur_tib_word/segpos_ekangyur_eTengyur_tib_word_invalid_data.json"  # noqa
    # Ensure the parent directory of the output files exists
    os.makedirs(os.path.dirname(valid_output_file), exist_ok=True)
    os.makedirs(os.path.dirname(invalid_output_file), exist_ok=True)
    process_folder(folder_path, valid_output_file, invalid_output_file)
