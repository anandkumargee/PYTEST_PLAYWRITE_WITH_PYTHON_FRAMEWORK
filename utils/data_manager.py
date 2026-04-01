import json
import os

class DataManager:
    @staticmethod
    def load_json(filename):
        file_path = os.path.join(os.getcwd(), "data", filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")
        with open(file_path, 'r') as f:
            return json.load(f)
