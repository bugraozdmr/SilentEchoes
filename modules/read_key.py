import os
from pathlib import Path

def load_key(key_path = Path(__file__).parent.parent / 'key' / 'secret.key'):
    if not os.path.isfile(key_path):
        raise FileNotFoundError(f"File can not found: {key_path}")

    try:
        with open(key_path, 'rb') as key_file:
            return key_file.read()
    except IOError as e:
        raise RuntimeError(f"File can not read: {e}")