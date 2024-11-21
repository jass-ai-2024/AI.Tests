from automatic_tests_generation.openapi_file_processing import FileProcessing

link = "....git"
file_processor_and_test_generator = FileProcessing(link)
file_processor_and_test_generator.tests_generation()
tests = file_processor_and_test_generator.get_generated_tests()

print(tests, len(tests), *tests, sep="\n\n\n")
