import os
import re
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


def load_json_header(filename):
    """
    Load a JSON header from the 'headers' directory. It replaces environment variables inside
    header JSON input files.
    :param filename: Name of the JSON file.
    :return: Dictionary representing the JSON file.
    """
    filepath = join(Path(__file__).parent.parent, 'headers', filename)

    if not isfile(filepath):
        raise FileNotFoundError(f"Payload file '{filename}' not found in 'payloads/' directory.")
    with open(filepath, 'r', encoding='utf-8') as file:
        headers_raw = load(file)

    pattern = re.compile(r"\{\{(\w+)\}\}")
    headers_replaced = {}
    for key, value in headers_raw.items():
        matches = pattern.findall(value)
        for var_name in matches:
            var_value = os.getenv(var_name)
            if var_value:
                value = value.replace(f"{{{{{var_name}}}}}", var_value)
            else:
                raise ValueError(f"Environment variable '{var_name}' does not exists.")
        headers_replaced[key] = value

    return headers_replaced


def extract_curly_vars(input_string):
    return re.findall(r'\{([\w]+)\}', input_string)
