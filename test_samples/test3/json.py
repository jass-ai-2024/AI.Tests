# должно пройти
import json

def create_json_file(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)
    return f"File {file_name} created successfully."

