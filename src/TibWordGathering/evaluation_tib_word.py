import json
import os


def read_and_process_tibetan_data(file_path, encoding="utf-16"):
    """
    Reads the Tibetan labeled data file, processes each line, and returns a list of dictionaries.
    Each dictionary contains 'source' and 'target' keys, where 'source' is the original sentence text
    and 'target' is the tokenized words separated by spaces.

    Parameters:
    file_path (str): The path to the Tibetan labeled data file.
    encoding (str): The encoding of the file. Defaults to 'utf-16'.

    Returns:
    list: A list of dictionaries, each containing 'source' and 'target' keys.
    """
    with open(file_path, encoding=encoding) as file:
        lines = file.readlines()

    # Prepare the JSON structure
    json_data = []

    for line in lines:
        # Strip whitespace and split by newline
        line = line.strip()
        if line:  # Check if the line is not empty
            words = line.split("/")
            source = "".join(words)  # Join words to form the source sentence
            target = " ".join(words)  # Join words with space for the target
            json_data.append({"source": source, "target": target})

    return json_data


def write_json_to_file(
    data, output_folder, output_file_name="evaluate.json", encoding="utf-8"
):
    """
    Writes the given list of data to a JSON file.

    Parameters:
    data (list): A list of data to be written to the JSON file.
    output_folder (str): The path to the folder where the output JSON file will be saved.
    output_file_name (str): The name of the output JSON file. Defaults to 'evaluate.json'.
    encoding (str): The encoding of the output file. Defaults to 'utf-8'.
    """
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, output_file_name)
    with open(output_file, "w", encoding=encoding) as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# Example usage
file_path = "data/input/Tibetan/Tibetan_labeled_2.5w.txt"
output_folder = "data/output/evaluate_tib_word"
data = read_and_process_tibetan_data(file_path)
write_json_to_file(data, output_folder)
