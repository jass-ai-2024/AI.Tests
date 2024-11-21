from AutomaticTestsGeneration.openapi_file_processing import FileProcessing
import os


def save_tests_to_files(tests, directory="__autotests"):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    target_directory = os.path.join(script_directory, directory)
    os.makedirs(target_directory, exist_ok=True)

    for i, test_code in enumerate(tests):
        file_name = os.path.join(directory, f"test_{i + 1}.py")
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(test_code[9:-3])
            print(f"Saved: {file_name}")
        except Exception as e:
            print(f"Failed to save {file_name}. Error: {e}")


def main(dir):
    file_processor_and_test_generator = FileProcessing(dir)
    file_processor_and_test_generator.tests_generation()
    tests = file_processor_and_test_generator.get_generated_tests()
    save_tests_to_files(tests)
    return tests
