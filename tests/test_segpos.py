import json

from TibWordGathering.segpos import process_file


def test_segpos():
    """
    This function tests the equality of the source text in the input file with the source in the JSON files.
    It checks if the source text from the input file matches the source in the JSON files.
    It also saves the valid data to a JSON file for further inspection.
    """
    input_file_path = "tests/data/segpos_sample/segpos.txt"
    output_file_path = "tests/data/expected/segpos.json"
    valid_output_path = "tests/data/actual/valid_data.json"  # Path to save valid data

    # Load the valid source texts from the .txt file using the segpos parser
    valid_data, _ = process_file(input_file_path)

    # Convert valid_data into a format similar to JSON for comparison
    valid_data_json_format = [
        {"source": item["source"], "target": item["target"]} for item in valid_data
    ]

    # Save the valid data to a JSON file
    with open(valid_output_path, "w", encoding="utf-8") as valid_file:
        json.dump(valid_data_json_format, valid_file, ensure_ascii=False, indent=2)

    with open(output_file_path, encoding="utf-8") as expected_file:
        expected_data = json.load(expected_file)

    assert (
        valid_data_json_format == expected_data
    ), f"Mismatch between processed data and expected data.\nProcessed: {valid_data_json_format}\nExpected: {expected_data}"  # noqa
