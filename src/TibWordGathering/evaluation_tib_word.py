import os
from pathlib import Path

from TibWordGathering.utils import is_valid_data_point, save_json


def read_and_process_tibetan_data(file_path, encoding="utf-16"):
    """
    Reads the Tibetan labeled data file, processes each line, and returns a list of dictionaries.
    Each dictionary contains 'source', 'target', and 'filename' keys, where 'source' is the original sentence text,
    'target' is the tokenized words separated by spaces, and 'filename' is the name of the processed file.
    """
    with open(file_path, encoding=encoding) as file:
        lines = file.readlines()

    # Prepare the lists for valid and invalid data
    valid_data = []
    invalid_data = []

    # Extract filename
    filename = os.path.basename(file_path)

    for line in lines:
        # Strip whitespace and split by slash
        line = line.strip()
        if line:  # Check if the line is not empty
            words = line.split("/")
            source = "".join(words)  # Join words to form the source sentence
            target = " ".join(
                [word for word in words if word]
            )  # Join words with space but skip empty strings

            # Create a dictionary with source, target, and filename
            data_point = {"source": source, "target": target, "filename": filename}

            # Classify data as valid or invalid based on criteria
            if is_valid_data_point(data_point):
                valid_data.append(data_point)
            else:
                invalid_data.append(data_point)

    return valid_data, invalid_data


if __name__ == "__main__":
    # Define paths
    folder_path = "data/input/Tibetan"
    output_folder = Path("data/output/evaluate_tib_word")
    os.makedirs(output_folder, exist_ok=True)

    # Output JSON files for valid and invalid data
    valid_output_data_file = output_folder / "evaluate_valid_data.json"
    invalid_output_data_file = output_folder / "evaluate_invalid_data.json"

    # Initialize lists to store all valid and invalid data
    all_valid_data = []
    all_invalid_data = []

    # Process each file in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)

            # Read and process the file
            valid_data, invalid_data = read_and_process_tibetan_data(file_path)

            # Append to the final list of valid and invalid data
            all_valid_data.extend(valid_data)
            all_invalid_data.extend(invalid_data)

    # Save all valid data into a single JSON file
    save_json(all_valid_data, valid_output_data_file)

    # Save all invalid data into a separate JSON file
    if all_invalid_data:
        save_json(all_invalid_data, invalid_output_data_file)
