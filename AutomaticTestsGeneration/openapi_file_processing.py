from AutomaticTestsGeneration.openapi_file_finder import ArtefactTestsFinder
from AutomaticTestsGeneration.tests_generator import TestGeneration


class FileProcessing:
    def __init__(self, directory_link):
        self.repo_url = directory_link
        self.__generated_tests = list()

    def tests_generation(self):
        finder = ArtefactTestsFinder(self.repo_url)
        test_gen = TestGeneration()
        file_content = finder.get_file_content()

        if file_content:
            for i in file_content["paths"]:
                new_file_content = {
                    'openapi': file_content["openapi"],
                    'info': file_content["info"],
                    'paths': {str(i): file_content["paths"][i]}
                }
                generated_test = test_gen.chat_conversation(new_file_content)
                self.__generated_tests.append(generated_test)

    def get_generated_tests(self):
        return self.__generated_tests
