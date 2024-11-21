#!/usr/bin/env python3

import subprocess
import sys
import os
import time
import requests
import json

def check_openapi_endpoint(workspace_dir):
    max_retries = 30
    retry_interval = 1

    for _ in range(max_retries):
        try:
            response = requests.get('http://localhost:9000/openapi.json')
            if response.status_code == 200:
                print(f"Version endpoint responded with: {response.text}")
                output_file = os.path.join(workspace_dir, "openapi.json")
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=4)
                print(f"Info saved into {output_file}")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(retry_interval)
        print("Waiting for service to be ready...")

    print("Service failed to respond correctly")
    return False

def run_command(command, workdir):
    """
    Run a shell command and return the result
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            cwd=workdir,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Exit code: {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def check_required_files(workspace_dir):
    """
    Check if required files (main.py and requirements.txt) exist in the workspace
    """
    required_files = ['docker-compose.yml', 'docker-compose.yaml', 'compose.yml', 'compose.yaml']
    missing_files = []

    for file in required_files:
        file_path = os.path.join(workspace_dir, file)
        if os.path.isfile(file_path):
            return True

    print(f"Error: Missing compose file")
    return False


def main(workspace_dir):
    print("Starting smoke test...")

    # Check for required files
    print("Checking for required files...")
    if not check_required_files(workspace_dir):
        print("Smoke test failed: Missing docker-compose file")
        return (False, "Smoke test failed: Missing required files")

    # Run the Docker container
    print("Running Docker container...")

    if not run_command("docker compose up", workspace_dir):
        print("Failed to run compose")
        return (False, "Failed to start container")

    # Check if the service responds correctly
    print("Testing /version endpoint...")
    if not check_version_endpoint():
        print("Version endpoint test failed")
        run_command("docker compose down", workspace_dir)
        return (False, "Version endpoint test failed")

    print("Smoke test completed successfully!")
    run_command("docker compose down", workspace_dir)
    return (True, "Smoke test completed successfully!")

if __name__ == "__main__":
    main(sys.argv[1])
