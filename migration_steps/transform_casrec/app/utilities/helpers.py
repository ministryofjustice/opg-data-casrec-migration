import os


def get_mapping_file(file_name: str) -> str:
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, f"../mapping_definitions/{file_name}.json")

    return file_path


def log_title(message: str) -> str:
    total_length = 100
    longest_word = 12

    padded_word = "  " + message + " " * (longest_word - len(message) + 2)

    left_filler_length = round((total_length) / 2) - longest_word

    right_filler_length = total_length - len(padded_word) - left_filler_length

    left_filler = "=" * left_filler_length
    right_filler = "=" * right_filler_length

    log_string = left_filler + padded_word.upper() + right_filler

    return log_string
