import os
import json
import tempfile


class ArtefactTestsFinder:
    def __init__(self, directory_link):
        self.__repo_url = directory_link
        self.__file_name = "openapi.json"
        self.__file_path = None
        self.__file_content = None

    def __find_artefact(self):
        if not os.path.exists(self.__repo_url):
            raise Exception(f"The directory '{self.__repo_url}' does not exist.")

        for root, dirs, files in os.walk(self.__repo_url):
            if self.__file_name in files:
                file_path = os.path.join(root, self.__file_name)
                # self.__file_path = os.path.join(root, self.__file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.__file_content = data
                    self.__file_path = file_path

    def get_file_content(self):
        self.__find_artefact()
        return self.__file_content
