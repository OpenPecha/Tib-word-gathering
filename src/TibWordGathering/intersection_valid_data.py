import json
import os

from TibWordGathering.utils import read_json_file, save_json


# Function to find the intersection based on the 'source' field
def find_intersection(file1, file2):
    set1 = {entry["source"] for entry in file1}
    set2 = {entry["source"] for entry in file2}
    common_sources = set1.intersection(set2)

    # Filter the entries that are common in both JSON files
    intersection = [entry for entry in file1 if entry["source"] in common_sources]
    return intersection


def main():
    # File paths for the two JSON files (replace with actual file paths)
    valid_oversegmented_data_file = "data/output/overseg_valid_word_seg_data/overseg_valid_data.json"  # Replace with actual file path
    valid_undersegmented_data_file = (
        "data/output/valid_undersegmented.json"  # Replace with actual file path
    )
    final_valid_data_file = (
        "data/output/combine_intersection_data/combined_intersection.json"
    )

    # Load the JSON files
    file1 = read_json_file(valid_oversegmented_data_file)
    file2 = read_json_file(valid_undersegmented_data_file)

    # Ensure both files were loaded correctly
    if file1 is None or file2 is None:
        return

    # Print the number of entries in each file
    print(f"Number of entries in {valid_oversegmented_data_file}: {len(file1)}")
    print(f"Number of entries in {valid_undersegmented_data_file}: {len(file2)}")

    # Find the intersection of the two JSON files based on 'source'
    intersection_data = find_intersection(file1, file2)

    # Print the number of entries in the final intersection data
    print(f"Number of entries in final combined intersection: {len(intersection_data)}")

    # Save the intersection result to a new JSON file
    save_json(intersection_data, final_valid_data_file)


if __name__ == "__main__":
    main()
