from AutomaticTestsGeneration.openapi_file_processing import FileProcessing


def main(dir):
    file_processor_and_test_generator = FileProcessing(dir)
    file_processor_and_test_generator.tests_generation()
    tests = file_processor_and_test_generator.get_generated_tests()
    return tests

