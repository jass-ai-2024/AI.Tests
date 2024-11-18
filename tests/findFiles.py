# должно пройти
import os

def find_files_by_extension(directory, extension):
    return [f for f in os.listdir(directory) if f.endswith(extension)]

