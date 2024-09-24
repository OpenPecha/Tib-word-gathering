import os
from pathlib import Path

from TibWordGathering.utils import is_valid_data_point, save_json


def read_and_process_tibetan_data(file_path, encoding="utf-16"):
    """
    Reads the Tibetan labeled data file, processes each line, and returns a list of dictionaries.
    Each dictionary contains 'source' and 'target' keys, where 'source' is the original sentence text
    and 'target' is the tokenized words separated by spaces.
    """
    with open(file_path, encoding=encoding) as file:
        lines = file.readlines()

    # Prepare the JSON structure
    valid_data = []
    invalid_data = []

    for line in lines:
        # Strip whitespace and split by newline
        line = line.strip()
        if line:  # Check if the line is not empty
            words = line.split("/")
            source = "".join(words)  # Join words to form the source sentence
            target = " ".join(words)  # Join words with space for the target
            data_point = {"source": source, "target": target}
            if is_valid_data_point(data_point):
                valid_data.append(data_point)
            else:
                invalid_data.append(data_point)

    return valid_data, invalid_data


if __name__ == "__main__":
    # Example usage
    file_path = "data/input/Tibetan/Tibetan_labeled_2.5w.txt"
    output_folder = Path("data/output/evaluate_tib_word")
    os.makedirs(output_folder, exist_ok=True)
    valid_output_data_folder = output_folder / "valid_data_json"
    os.makedirs(valid_output_data_folder, exist_ok=True)
    invalid_output_data_folder = output_folder / "invalid_data_json"
    os.makedirs(invalid_output_data_folder, exist_ok=True)
    valid_data, invalid_data = read_and_process_tibetan_data(file_path)
    filename = os.path.basename(file_path).replace(".txt", ".json")
    save_json(valid_data, valid_output_data_folder / filename)
    if invalid_data:
        save_json(invalid_data, invalid_output_data_folder / filename)
