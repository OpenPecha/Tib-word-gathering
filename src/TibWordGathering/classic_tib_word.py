import json
import os


def parse_conllu(conllu_content):
    """
    Parses the given CoNLL-U content and returns a list of data.
    Each data is a dictionary with 'source' and 'target' as keys.
    The 'source' key contains the original sentence text, and the 'target' key contains the tokenized words.

    Parameters:
    conllu_content (str): The content of the CoNLL-U file.

    Returns:
    list: A list of data, each data being a dictionary with 'source' and 'target' keys.
    """
    data = []
    current_data = {"source": "", "target": ""}

    for line in conllu_content.split("\n"):
        if line.startswith("# text ="):
            if current_data["source"]:
                data.append(current_data)
                current_data = {"source": "", "target": ""}
            current_data["source"] = line.split("=", 1)[1].strip()
        elif line and not line.startswith("#"):
            parts = line.split("\t")
            if len(parts) > 1:
                word = parts[1]
                current_data["target"] += word + " "

    if current_data["source"]:
        data.append(current_data)

    # Remove extra spaces and trailing space in target
    for item in data:
        item["target"] = item["target"].strip()

    return data


def process_conllu_file(file_path, output_folder):
    """
    Processes a single CoNLL-U file and saves the results to a separate JSON file.
    Each data is a dictionary with 'source' and 'target' as keys.
    The 'source' key contains the original sentence text, and the 'target' key contains the tokenized words.

    Parameters:
    file_path (str): The path to the CoNLL-U file.
    output_folder (str): The path to the folder where the output JSON file will be saved.
    """
    with open(file_path, encoding="utf-8") as file:
        conllu_content = file.read()

    data = parse_conllu(conllu_content)
    filename = os.path.basename(file_path).split(".")[0] + ".json"
    output_file = os.path.join(output_folder, filename)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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
            process_conllu_file(file_path, output_folder)


# Example usage:
folder_path = "data/input/classical-tibetan-corpus-master/conllu"
output_folder = "data/output/classic_tib_word"
process_conllu_folder(folder_path, output_folder)
