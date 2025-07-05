import json
import os

# Path to your input.json file (in the same directory as this script)
INPUT_JSON_PATH = os.path.join(os.path.dirname(__file__), 'input.json')

def load_input_json():
    with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
