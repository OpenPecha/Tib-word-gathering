import json
from pathlib import Path

from TibWordGathering.conllu_parser import process_conllu_file


def test_conllu_parser():
    """
    This function tests the equality of the source text in the input file with the source in the JSON files.
    It checks if the source text from the input file matches the source in the expected JSON files.
    It also saves the valid data to a JSON file for further inspection.
    """
    input_file_path = "tests/data/conllu_sample/conllu.conllu"
    output_file_path = "tests/data/expected/conllu.json"
    valid_output_path = Path("tests/data/output")  # Path to save valid data
    valid_output_path.mkdir(parents=True, exist_ok=True)
    valid_output_data = valid_output_path / "conllu_data.json"

    # Load the valid source texts from the .conllu file using the conllu parser
    valid_data, _ = process_conllu_file(input_file_path)

    # Convert valid_data into JSON-like format for comparison
    valid_data_json_format = [
        {"source": item["source"], "target": item["target"]} for item in valid_data
    ]

    # Save the valid data to a JSON file (for inspection, not strictly necessary for the test itself)
    with open(valid_output_data, "w", encoding="utf-8") as valid_output_file:
        json.dump(
            valid_data_json_format, valid_output_file, ensure_ascii=False, indent=2
        )

    # Load the expected data from the expected JSON output file
    with open(output_file_path, encoding="utf-8") as expected_output_file:
        expected_data = json.load(expected_output_file)

    # Compare the source and target fields in valid_data and expected_data
    assert (
        valid_data_json_format == expected_data
    ), f"Mismatch between processed data and expected data.\nProcessed: {valid_data_json_format}\nExpected: {expected_data}"  # noqa

    print("Test passed: The source and target fields match the expected output.")


# You can run this test using pytest or unittest, or manually call it if needed
if __name__ == "__main__":
    test_conllu_parser()
