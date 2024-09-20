import json
import os
from typing import List


def process_file(file_path: str) -> List[dict]:
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
                        data.append(
                            {
                                "source": source,
                                "target": target,
                            }
                        )
                        current_sentence = []
                elif word.startswith("p") and word[1:].isdigit():
                    # Found a page number within the text
                    if current_sentence:
                        # Save the current sentence before changing the page
                        source = "".join(current_sentence)
                        target = " ".join(current_sentence)
                        data.append(
                            {
                                "source": source,
                                "target": target,
                            }
                        )
                    current_sentence = []
                else:
                    current_sentence.append(word)

    # Handle any remaining sentence
    if current_sentence:
        source = "".join(current_sentence)
        target = " ".join(current_sentence)
        data.append(
            {
                "source": source,
                "target": target,
            }
        )

    return data


def process_folder(folder_path: str):
    """
    Processes all text files in the given folder and saves the results to separate JSON files.
    Each JSON file name is the same as the original file name.

    Parameters:
    folder_path (str): The path to the folder containing text files.
    """
    output_folder = "data/output/segpos_tib_word"
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            data = process_file(file_path)
            output_file = os.path.join(output_folder, filename.replace(".txt", ".json"))
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)


# Example usage:
folder_path = "data/input/SegPOS-DharmaDownload_July2020/seg"
process_folder(folder_path)
