import os
from typing import List

from TibWordGathering.utils import is_valid_data_point, save_json


def process_file(file_path: str):
    """
    Processes a single text file and returns a list of data.
    Each data is a dictionary with 'source' and 'target' as keys.
    The 'source' key contains the original sentence text, and the 'target' key contains the tokenized words.

    Parameters:
    file_path (str): The path to the text file.

    Returns:
    list: A list of data, each data being a dictionary with 'source' and 'target' keys.
    """
    data: List[dict] = []
    invalid_data: List[dict] = []
    current_sentence: List[str] = []

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
        data_point = {
            "source": source,
            "target": target,
        }
        if is_valid_data_point(data_point):
            data.append(data_point)
        else:
            invalid_data.append(data_point)

    return data, invalid_data


def process_folder(folder_path: str):
    """
    Processes all text files in the given folder and saves the results to separate JSON files.
    Each JSON file name is the same as the original file name.

    Parameters:
    folder_path (str): The path to the folder containing text files.
    """
    valid_output_folder = (
        "data/output/segpos_ekangyur_eTengyur_tib_word/valid_data_json"
    )
    os.makedirs(valid_output_folder, exist_ok=True)

    invalid_output_folder = (
        "data/output/segpos_ekangyur_eTengyur_tib_word/invalid_data_json"
    )
    os.makedirs(invalid_output_folder, exist_ok=True)
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            for filename in os.listdir(os.path.join(root, dir)):
                if filename.endswith(".txt"):
                    file_path = os.path.join(root, dir, filename)
                    data, invalid_data = process_file(file_path)
                    valid_output_file = os.path.join(
                        valid_output_folder,
                        f"{dir}_{filename.replace('.txt', '.json')}",
                    )
                    save_json(data, valid_output_file)
                    if invalid_data:
                        invalid_data_file = os.path.join(
                            invalid_output_folder,
                            f"{dir}_{filename.replace('.txt', '.json')}",
                        )
                        save_json(invalid_data, invalid_data_file)


# Example usage:
folder_path = "data/input/SegPos-eKangyur-eTengyur"
process_folder(folder_path)
