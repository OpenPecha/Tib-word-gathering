import os

from TibWordGathering.utils import read_json_file
from TibWordGathering.word_seg_validation import validate_word_segmentation


def test_word_seg_validation():
    unique_word_list_file = (
        "tests/data/input/unique_word_list/combined_unique_tibetan_word_list.json"
    )
    word_segmentation_data_file = "tests/data/input/word_seg_data.json"
    validated_word_segmentation_file = "tests/data/output/test_validated_word_seg_data/test_validated_word_seg_data.json"  # noqa
    invalidated_word_segmentation_file = "tests/data/output/test_invalidated_word_seg_data/test_invalidated_word_seg_data.json"  # noqa

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
    word_segmentation_data = read_json_file(word_segmentation_data_file)
    word_list = read_json_file(unique_word_list_file)
    validate_word_segmentation(
        word_segmentation_data,
        word_list,
        validated_word_segmentation_file,
        invalidated_word_segmentation_file,
        chunk_size=5,
        checkpoint_interval=2,
    )
