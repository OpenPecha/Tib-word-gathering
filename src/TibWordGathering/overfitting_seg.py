import json
import os
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Tuple

from tqdm import tqdm

from TibWordGathering.utils import append_to_json_file, read_json_file


def find_invalid_combinations(tokens: List[str], word_set: set) -> List[str]:
    """
    Find all invalid combinations within the tokens.
    A combination is invalid if it's present in the word_set.
    Combinations can be 2 to 4 consecutive tokens.
    """
    """_summary_

    Returns:
        _type_: _description_
    """
    invalid_combos = []
    n = len(tokens)

    for i in range(n):
        for combo_length in range(2, 5):
            if i + combo_length <= n:
                combo = "".join(tokens[i : i + combo_length])
                if combo in word_set:
                    invalid_combos.append(combo)
    return invalid_combos


def process_batch(
    data_batch: List[Dict], word_set: set
) -> Tuple[List[Dict], List[Dict]]:
    """
    Process a batch of entries.
    """
    valid_entries = []
    invalid_entries = []

    for entry in data_batch:
        tokens = entry["target"].split()
        invalid_combos = find_invalid_combinations(tokens, word_set)

        if invalid_combos:
            invalid_entry = entry.copy()
            invalid_entry["matched_combinations"] = invalid_combos
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
    valid_output_path = (
        "data/output/overseg_valid_word_seg_data/overseg_valid_data.json"
    )
    invalid_output_path = (
        "data/output/overseg_invalidated_word_seg_data/oveerseg_invalid_data.json"
    )

    # Ensure output directories exist
    validated_output_dir = os.path.dirname(valid_output_path)
    invalid_output_dir = os.path.dirname(invalid_output_path)
    for directory in [validated_output_dir, invalid_output_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

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
