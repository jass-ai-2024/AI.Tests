import os
import re
import time
import shutil
from typing import Tuple
import Linter.input_code_check as linter
import SmokeTest.smoke_test as smoke_test

def find_project_folders(directory: str) -> list[str]:
    """Find folders matching project_v[0-9]* pattern"""
    pattern = re.compile(r"project_v\d+$")
    return [
        f for f in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, f)) and pattern.match(f)
    ]

def should_run_tests(project_path: str) -> bool:
    """Check if tests should be run for this project"""
    generation_done = os.path.exists(os.path.join(project_path, "GENERATION_DONE"))
    tests_done = os.path.exists(os.path.join(project_path, "TESTS_DONE"))
    return generation_done and not tests_done

def write_results_file(project_path: str, filename: str, content: str) -> None:
    """Write test results to a file"""
    with open(os.path.join(project_path, filename), "w") as f:
        f.write(content)

def run_tests(project_path: str) -> Tuple[bool, bool]:
    """Run linter and smoke tests, return (linter_passed, smoke_passed)"""
    # Run linter
    linter_passed, linter_msg = linter.main(project_path)
    if not linter_passed:
        write_results_file(project_path, "LINTER_RESULTS", linter_msg)

    # Run smoke test
    smoke_passed, smoke_msg = smoke_test.main(project_path)
    if not smoke_passed:
        write_results_file(project_path, "SMOKE_TEST_RESULTS", smoke_msg)

    return linter_passed, smoke_passed

def copy_to_blackbox(project_path: str) -> None:
    """Copy project to blackbox and create deployment flag"""
    artf_id = os.getenv("ARTF_ID")
    if not artf_id:
        raise ValueError("ARTF_ID environment variable not set")

    # Create blackbox directories if they don't exist
    artifacts_dir = os.path.join("blackboard", "artfs")
    deploy_dir = os.path.join("blackboard", "deploy")
    os.makedirs(artifacts_dir, exist_ok=True)
    os.makedirs(deploy_dir, exist_ok=True)

    # Copy project contents
    target_dir = os.path.join(artifacts_dir, artf_id)
    shutil.copytree(project_path, target_dir)

    # Create deployment flag
    deploy_flag = os.path.join(deploy_dir, f"ready_to_deploy.{artf_id}")
    with open(deploy_flag, "w") as f:
        f.write("")

def process_project(project_path: str) -> None:
    """Process a single project folder"""
    linter_passed, smoke_passed = run_tests(project_path)

    if linter_passed and smoke_passed:
        write_results_file(project_path, "TESTS_PASSED", "All tests passed successfully")
        copy_to_blackbox(project_path)

    # Mark tests as done regardless of outcome
    write_results_file(project_path, "TESTS_DONE", "")

def main() -> None:
    """Main agent loop"""
    while True:
        project_folders = find_project_folders(".")

        for folder in project_folders:
            project_path = os.path.join(".", folder)
            if should_run_tests(project_path):
                print(f"Processing project: {folder}")
                try:
                    process_project(project_path)
                except Exception as e:
                    print(f"Error processing {folder}: {str(e)}")

        time.sleep(2)

if __name__ == "__main__":
    main()
