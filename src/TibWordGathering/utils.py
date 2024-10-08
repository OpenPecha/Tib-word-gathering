import json
import os
from typing import Dict, List


# Function to calculate Manhattan distance between two strings
def manhattan_distance(str1, str2):
    if len(str1) != len(str2):
        return -1  # Return -1 to indicate unequal lengths
    distance = 0
    for c1, c2 in zip(str1, str2):
        if c1 != c2:
            distance += 1  # Increment distance if characters differ
    return distance


# Function to validate if the source and target match after removing spaces
def is_valid_data_point(data_point):
    # Remove spaces from both source and target
    source = data_point["source"].replace(" ", "")
    target = data_point["target"].replace(" ", "")

    # Check if lengths are equal after space removal
    if len(source) != len(target):
        return False

    # Calculate Manhattan distance between source and target
    distance = manhattan_distance(source, target)

    # Return True if the distance is 0, meaning the strings are identical
    return distance == 0


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json_file(file_path):
    with open(file_path) as file:
        return json.load(file)


def write_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def append_to_json_file(data: List[Dict], output_path: str):
    """
    Append data to an existing JSON file or create a new one if it doesn't exist.
    """
    if os.path.exists(output_path):
        with open(output_path, "r+", encoding="utf-8") as file:
            existing_data = json.load(file)
            existing_data.extend(data)
            file.seek(0)  # Move cursor to start to overwrite file
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
    else:
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
