import json

from TibWordGathering.evaluate_tib_word import read_and_process_tibetan_data
from TibWordGathering.utils import save_json


def test_evaluate_tib_word():
    """
    This function tests the equality of the source text in the input file with the source in the JSON files.
    It checks if the source text from the input file matches the source in the JSON files.
    It also saves the valid data to a JSON file for further inspection.
    """
    input_file_path = "tests/data/evaluate_tibetan_sample/evaluate.txt"
    output_file_path = "tests/expected/evaluate.json"
    valid_output_path = (
        "tests/data/output/evaluate_data.json"  # Path to save valid data
    )

    # Load the valid source texts from the Tibetan labeled data file
    valid_data, invalid_data = read_and_process_tibetan_data(
        input_file_path, encoding="utf-16"
    )

    # Convert valid_data into a format similar to JSON for comparison
    valid_data_json_format = [
        {"source": item["source"], "target": item["target"]} for item in valid_data
    ]
    save_json(valid_data, valid_output_path)
    # Load the expected data from the expected JSON output file
    with open(output_file_path, encoding="utf-8") as expected_output_file:
        expected_data = json.load(expected_output_file)

    assert (
        valid_data_json_format == expected_data
    ), f"Mismatch between processed data and expected data.\nProcessed: {valid_data_json_format}\nExpected: {expected_data}"  # noqa
