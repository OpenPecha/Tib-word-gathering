import json
import os

from TibWordGathering.utils import is_valid_data_point, save_json


# Main function to process data points
def process_data(input_file, output_file_valid, output_file_invalid):
    # Ensure the output directory exists
    output_dir_valid = os.path.dirname(output_file_valid)
    output_dir_invalid = os.path.dirname(output_file_invalid)

    if not os.path.exists(output_dir_valid):
        os.makedirs(output_dir_valid)
        print(f"Created directory {output_dir_valid}")

    if not os.path.exists(output_dir_invalid):
        os.makedirs(output_dir_invalid)
        print(f"Created directory {output_dir_invalid}")

    # Load the data from the input file
    with open(input_file, encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    valid_data = []
    invalid_data = []

    # Add filename to each data point and validate it
    filename = os.path.basename(input_file)  # Extract filename from the input file path
    for data_point in data:
        data_point["filename"] = filename  # Add the filename field to each data point

        if is_valid_data_point(data_point):
            valid_data.append(data_point)
        else:
            invalid_data.append(data_point)

    # Save valid data to the output file
    save_json(valid_data, output_file_valid)
    print(f"Saved {len(valid_data)} valid data points to {output_file_valid}")

    # Save invalid data to the output file
    save_json(invalid_data, output_file_invalid)
    print(f"Saved {len(invalid_data)} invalid data points to {output_file_invalid}")


# Example usage
input_file = "data/input/Manual-dataset/manual_data.json"  # Your input file path
output_file_valid = "data/output/Manual-dataset/manual_data_valid_data.json"  # Where valid data will be stored
output_file_invalid = "data/output/Manual-dataset/manual_data_invalid_data.json"  # Where invalid data will be stored

process_data(input_file, output_file_valid, output_file_invalid)
