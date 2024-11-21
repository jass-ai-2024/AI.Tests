import os
import subprocess
import time
from typing import Tuple

def run_tests(project_path: str) -> Tuple[bool, str]:
    """Run all tests in the project using pytest"""
    tests_dir = os.path.join(project_path, "__autotests")
    if not os.path.exists(tests_dir):
        return False, "No tests directory found"

    failures = []

    try:
        # Start docker compose
        print("Starting docker compose...")
        subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True
        )

        # Wait for service to be ready
        print("Waiting for service to be ready...")
        time.sleep(5)

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
                ["docker", "compose", "down"],
                cwd=project_path,
                check=True,
                capture_output=True,
                text=True
            )
        except Exception as e:
            print(f"Error stopping docker compose: {e}")


def main(project_path: str) -> Tuple[bool, str]:
    """Main function to run tests"""
    return run_tests(project_path)
