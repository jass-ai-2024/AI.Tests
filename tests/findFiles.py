# должно пройти
import os

def find_files_by_extension(directory, extension):
    return [f for f in os.listdir(directory) if f.endswith(extension)]

if __name__ == "__main__":
    directory = "."
    extension = ".py"
    print(find_files_by_extension(directory, extension))
