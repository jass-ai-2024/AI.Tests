import os
import subprocess
import time
from typing import Tuple
import requests

def wait_for_service():
    max_retries = 30
    retry_interval = 10

    for _ in range(max_retries):
        try:
            response = requests.get('http://localhost:9000/openapi.json')
            if response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(retry_interval)
        print("Waiting for service to be ready...")

def run_tests(project_path: str) -> Tuple[bool, str]:
    """Run all tests in the project using pytest"""
    tests_dir = os.path.join(project_path, "__autotests")
    if not os.path.exists(tests_dir):
        return False, "No tests directory found"

    failures = []

    try:
        # Start docker compose
        print("Starting docker compose...")
        process = subprocess.Popen(
            ["docker compose up"],
            cwd=project_path,
            shell=True,
        )

        # Wait for service to be ready
        print("Waiting for service to be ready...")
        wait_for_service()

        print("Running tests...")
        # Run all test files using pytest
        result = subprocess.run(
            ["python3", "-m", "pytest", tests_dir, "-v"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            failures.append("Test execution failed:")
            failures.append(result.stdout)
            failures.append(result.stderr)
            return False, "\n".join(failures)

        return True, ""

    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed: {e.cmd}\nOutput: {e.output}\nError: {e.stderr}"
        return False, error_msg

    except Exception as e:
        return False, f"Error running tests: {str(e)}"

    finally:
        # Stop docker compose
        print("Stopping docker compose...")
        try:
            subprocess.run(
                ["docker compose down"],
                cwd=project_path,
                shell=True,
            )
        except Exception as e:
            print(f"Error stopping docker compose: {e}")


def main(project_path: str) -> Tuple[bool, str]:
    """Main function to run tests"""
    return run_tests(project_path)
