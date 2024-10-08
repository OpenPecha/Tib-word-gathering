# TibWordGathering/word_seg_validation.py

import os
from functools import partial
from multiprocessing import Pool, cpu_count

from tqdm import tqdm

from TibWordGathering.utils import read_json_file, write_json_file


def process_batch(batch, word_set):
    """
    Processes a batch of word segmentation data points.

    Args:
        batch (list): A list of data points (dictionaries) to process.
        word_set (set): A set of unique words for validation.

    Returns:
        tuple: Two lists containing valid and invalid data points respectively.
    """
    valid_datapoints = []
    invalid_datapoints = []

    for data_point in batch:
        target_field = data_point.get("target", "")
        words_in_target = target_field.split(" ")
        missing_words = [
            word for word in words_in_target if word and word not in word_set
        ]

        if not missing_words:
            valid_datapoints.append(data_point)
        else:
            datapoint_with_missing = data_point.copy()
            datapoint_with_missing["missing_words"] = missing_words
            invalid_datapoints.append(datapoint_with_missing)

    return valid_datapoints, invalid_datapoints


def chunkify(data, chunk_size):
    """
    Splits the data into smaller chunks.

    Args:
        data (list): The complete list of data points.
        chunk_size (int): The number of data points per chunk.

    Returns:
        generator: A generator yielding data chunks.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def save_checkpoint(valid_file, invalid_file, valid_batch, invalid_batch):
    """
    Saves the current batch of valid and invalid data points to their respective JSON files.

    Args:
        valid_file (str): Path to the validated data JSON file.
        invalid_file (str): Path to the invalidated data JSON file.
        valid_batch (list): List of valid data points to append.
        invalid_batch (list): List of invalid data points to append.
    """
    # Save valid datapoints
    if valid_batch:
        if os.path.exists(valid_file):
            existing_valid = read_json_file(valid_file)
            existing_valid.extend(valid_batch)
            write_json_file(valid_file, existing_valid)
        else:
            write_json_file(valid_file, valid_batch)

    # Save invalid datapoints
    if invalid_batch:
        if os.path.exists(invalid_file):
            existing_invalid = read_json_file(invalid_file)
            existing_invalid.extend(invalid_batch)
            write_json_file(invalid_file, existing_invalid)
        else:
            write_json_file(invalid_file, invalid_batch)


def validate_word_segmentation(
    word_segmentation_data,
    word_list,
    validated_file,
    invalidated_file,
    chunk_size=1000,
    checkpoint_interval=5,
):
    """
    Validates word segmentation data in parallel batches with progress visualization and checkpointing.

    Args:
        word_segmentation_data (list): List of word segmentation data points.
        word_list (list): List of unique words for validation.
        validated_file (str): Path to save validated data points.
        invalidated_file (str): Path to save invalidated data points.
        chunk_size (int, optional): Number of data points per batch. Defaults to 1000.
        checkpoint_interval (int, optional): Number of batches to process before saving a checkpoint. Defaults to 5.

    Returns:
        tuple: Two lists containing all valid and invalid data points.
    """
    word_set = set(word_list)  # Convert to set for O(1) lookups
    batches = list(chunkify(word_segmentation_data, chunk_size))
    total_batches = len(batches)

    all_valid = []
    all_invalid = []

    with Pool(processes=cpu_count()) as pool:
        # Use tqdm to display a progress bar
        for i, result in enumerate(
            tqdm(
                pool.imap(partial(process_batch, word_set=word_set), batches),
                total=total_batches,
                desc="Validating Batches",
            )
        ):
            valid_batch, invalid_batch = result
            all_valid.extend(valid_batch)
            all_invalid.extend(invalid_batch)
            # Save checkpoint at specified intervals
            if (i + 1) % checkpoint_interval == 0 or (i + 1) == total_batches:
                save_checkpoint(
                    validated_file, invalidated_file, valid_batch, invalid_batch
                )
                print(
                    f"Checkpoint saved after processing batch {i + 1}/{total_batches}"
                )

    return all_valid, all_invalid


if __name__ == "__main__":
    # Define file paths
    unique_word_list_file = (
        "data/input/unique_word_list/combined_unique_tibetan_word_list.json"
    )
    word_segmentation_data_file = "data/input/deduplication_combine_words/deduplicated_combined_word_seg_data.json"
    validated_word_segmentation_file = (
        "data/output/validated_word_seg_data/validated_word_seg_data.json"
    )
    invalidated_word_segmentation_file = (
        "data/output/invalidated_word_seg_data/invalidated_word_seg_data.json"
    )

    # Ensure output directories exist
    validated_word_segmentation_dir = os.path.dirname(validated_word_segmentation_file)
    invalidated_word_segmentation_dir = os.path.dirname(
        invalidated_word_segmentation_file
    )
    for directory in [
        validated_word_segmentation_dir,
        invalidated_word_segmentation_dir,
    ]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: '{directory}'")

    # Load data
    print("Loading unique word list...")
    word_list = read_json_file(unique_word_list_file)
    print(f"Total unique words loaded: {len(word_list)}")

    print("Loading word segmentation data...")
    word_segmentation_data = read_json_file(word_segmentation_data_file)
    print(f"Total word segmentation data points loaded: {len(word_segmentation_data)}")

    # Validate word segmentation data with batching and parallel processing
    print("Validating word segmentation data...")
    valid_datapoints, invalid_datapoints = validate_word_segmentation(
        word_segmentation_data,
        word_list,
        validated_word_segmentation_file,
        invalidated_word_segmentation_file,
        chunk_size=1000,
        checkpoint_interval=5,
    )

    # Print summary information
    print("\nValidation Complete.")
    print(f"Total valid datapoints: {len(valid_datapoints)}")
    print(f"Total invalid datapoints: {len(invalid_datapoints)}")
