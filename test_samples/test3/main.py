from json import *
if __name__ == "__main__":
    data = {"name": "John Doe", "age": 30, "city": "New York"}
    print(create_json_file(data, "data.json"))
