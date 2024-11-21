import os
import json
from git import Repo
import tempfile


class ArtefactTestsFinder:
    def __init__(self, repo_url):
        self.__repo_url = repo_url
        self.__file_name = "../openapi.json"
        self.__file_path = None
        self.__file_content = None

    def __find_artefact(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                Repo.clone_from(self.__repo_url, tmp_dir)
            except Exception as e:
                raise Exception(f"No such repository. Error message: {e}")

            for root, dirs, files in os.walk(tmp_dir):
                if self.__file_name in files:
                    file_path = os.path.join(root, self.__file_name)
                    # self.__file_path = file_path

                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.__file_content = data

    def get_file_content(self):
        self.__find_artefact()
        return self.__file_content
