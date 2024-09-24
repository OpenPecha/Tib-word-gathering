import json


def is_valid_data_point(data_point):

    source = data_point["source"]
    target = data_point["target"].replace(" ", "")

    # Use simple length calculation instead of botok
    source_length = len(source)  # Length of source
    target_length = len(target)  # Length of target

    adjusted_target_length = target_length + source.count(" ")

    # Update the assert statement to include error details
    if source_length == adjusted_target_length:
        return True
    else:
        return False


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
