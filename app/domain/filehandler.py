import json
import os

class Createfile:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)

    def file(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def write_in_file(self, data):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
