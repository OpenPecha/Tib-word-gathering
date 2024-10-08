import json
import os
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Tuple

from tqdm import tqdm

from TibWordGathering.utils import append_to_json_file, read_json_file


def check_under_segmented_words(word: str, word_set: set) -> List[str]:
    """
    Check if any segments of the word (split by '་') are in the word set.
    Returns a list of segments that are in the word list (under-segmented).
    If the word ends with '་' but cannot be split further, it's considered valid.
    """
    segments = word.split("་")

    # If there's only one segment or the word ends with '་' and can't be split into more than one part, it's valid
    if len(segments) <= 1 or (len(segments) == 2 and segments[1] == ""):
        return []

    # Otherwise, check each segment to see if it's under-segmented
    under_segmented = [segment for segment in segments if segment in word_set]

    return under_segmented


def process_batch(
    data_batch: List[Dict], word_set: set
) -> Tuple[List[Dict], List[Dict]]:
    """
    Process a batch of entries.
    """
    valid_entries = []
    invalid_entries = []

    for entry in data_batch:
        tokens = entry[
            "target"
        ].split()  # Split target by spaces to get individual words
        under_segmented_words = []

        for word in tokens:
            under_segments = check_under_segmented_words(word, word_set)
            if under_segments:
                under_segmented_words.append(
                    {"word": word, "under_segmented": under_segments}
                )

        if under_segmented_words:
            invalid_entry = entry.copy()
            invalid_entry["under_segmented_words"] = under_segmented_words
            invalid_entries.append(invalid_entry)
        else:
            valid_entries.append(entry)

    return valid_entries, invalid_entries


def process_in_batches(
    data: List[Dict],
    word_set: set,
    batch_size: int,
    valid_output_path: str,
    invalid_output_path: str,
):
    """
    Process entries in batches with multiprocessing.
    """
    num_batches = (len(data) + batch_size - 1) // batch_size
    pool = Pool(cpu_count())

    for batch_num in tqdm(range(num_batches), desc="Processing batches"):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, len(data))
        data_batch = data[start_idx:end_idx]

        # Process the batch in parallel
        results = pool.apply_async(process_batch, (data_batch, word_set))
        valid_entries, invalid_entries = results.get()

        # Append results to the final JSON files after each batch
        append_to_json_file(valid_entries, valid_output_path)
        append_to_json_file(invalid_entries, invalid_output_path)

    pool.close()
    pool.join()


def main():
    # Define file paths
    word_list_path = (
        "data/input/unique_word_list/combined_unique_tibetan_word_list.json"
    )
    segmented_json_path = (
        "data/output/validated_word_seg_data/validated_word_seg_data.json"
    )
    valid_output_path = "data/output/valid_undersegmented.json"
    invalid_output_path = "data/output/invalid_undersegmented.json"

    # Ensure output directories exist
    validated_output_dir = os.path.dirname(valid_output_path)
    invalid_output_dir = os.path.dirname(invalid_output_path)
    for directory in [validated_output_dir, invalid_output_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Check if input files exist
    if not os.path.isfile(word_list_path):
        print(f"Error: Word list file '{word_list_path}' does not exist.")
        exit(1)
    if not os.path.isfile(segmented_json_path):
        print(f"Error: Segmented JSON file '{segmented_json_path}' does not exist.")
        exit(1)

    # Load data
    word_list = read_json_file(word_list_path)
    segmented_data = read_json_file(segmented_json_path)

    # Process in batches
    batch_size = 1000  # Set batch size
    process_in_batches(
        segmented_data,
        set(word_list),
        batch_size,
        valid_output_path,
        invalid_output_path,
    )

    print("\nProcessing Complete!")


if __name__ == "__main__":
    main()
