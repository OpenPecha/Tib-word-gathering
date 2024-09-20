import json
import os


def test_remove_space_from_target():
    """
    This function tests the removal of spaces from the target in the JSON files.
    It checks for length mismatches and asserts that the adjusted target length matches the source length.
    """
    folder_paths = [
        "data/output/evaluate_tib_word",
        "data/output/segpos_tib_word",
        "data/output/classic_tib_word",
    ]
    for folder_path in folder_paths:
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    source = item["source"]
                    target = item["target"].replace(" ", "")
                    space_count = source.count(" ")
                    adjusted_target_length = len(target) + space_count
                    assert adjusted_target_length == len(source)
