import os
import subprocess
import tempfile
from typing import List, Tuple


class RunUnusedCheckTests:
    def __init__(self, file_or_directory_path: str):
        self.file_or_directory_path = file_or_directory_path
        self.__pylint_check = True
        self.__flake8_check = True
        self.__deadcode_check = True
        self.__mypy_check = True
        self.__errors = list()

    def __run_pylint(self):
        try:
            result = subprocess.run(
                ["pylint", self.file_or_directory_path, "--disable=C,R"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                self.__pylint_check = False
                for error in result.stdout.splitlines():
                    self.__errors.append(error)
        except Exception as e:
            self.__pylint_check = False
            self.__errors.append(f"Error running pylint: {e}")

    def __run_flake8(self):
        try:
            result = subprocess.run(
                ["flake8", self.file_or_directory_path],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                self.__flake8_check = False
                self.__errors.append(result.stdout.splitlines())
        except Exception as e:
            self.__flake8_check = False
            self.__errors.append(f"Error running flake8: {e}")

    def __run_deadcode(self):
        try:
            command = f"deadcode {self.file_or_directory_path}"
            all_correct_message = "\x1b[1mWell done!\x1b[0m ✨ 🚀 ✨\n"
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=False
            )
            if result.stdout != all_correct_message:
                self.__deadcode_check = False
                self.__errors.append(result.stdout.splitlines())
        except Exception as e:
            self.__deadcode_check = False
            self.__errors.append(f"Error running deadcode: {e}")

    def __run_mypy(self):
        try:
            result = subprocess.run(
                ["mypy", "--strict", self.file_or_directory_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(result)
            if result.returncode != 0:
                self.__mypy_check = False
                self.__errors.append(result.stdout.splitlines())
        except Exception as e:
            self.__mypy_check = False
            self.__errors.append(f"Error running mypy: {e}")

    def analyze_code(self):
        tools = {
            "Pylint": self.__run_pylint,
            "Flake8": self.__run_flake8,
            "DeadCode": self.__run_deadcode,
            "Mypy": self.__run_mypy,
        }
        for tool_name, tool_func in tools.items():
            print(f"Running {tool_name}...")
            tool_func()

        if self.__pylint_check & self.__flake8_check & self.__deadcode_check & self.__mypy_check:
            print("All tests Passed!")
        else:
            print("Some tests failed. Check them below:")
            for failed_test in self.__errors:
                print(failed_test)

    def return_status(self):
        is_tests_ok = self.__pylint_check & self.__flake8_check & self.__deadcode_check & self.__mypy_check
        message = str(self.__errors) if len(self.__errors) > 0 else "OK!"
        return is_tests_ok, message


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python analyze_code.py <path_to_file_or_directory>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"Error: The path '{path}' does not exist.")
        sys.exit(1)

    tester = RunUnusedCheckTests(path)
    test_run = tester.analyze_code()
    test_results = tester.return_status()

