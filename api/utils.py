from pathlib import Path
from os.path import isfile, join
from json import load


def load_json_payload(filename):
    """
    Load a JSON payload from the 'payloads' directory.
    :param filename: Name of the JSON file.
    :return: Dictionary representing the JSON payload.
    """
    filepath = join(Path(__file__).parent.parent, 'payloads', filename)

    if not isfile(filepath):
        raise FileNotFoundError(f"Payload file '{filename}' not found in 'payloads/' directory.")
    with open(filepath, 'r', encoding='utf-8') as file:
        return load(file)
