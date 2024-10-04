import json


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
