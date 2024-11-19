#!/usr/bin/env python3

import subprocess
import sys
import os
import time
import requests
import json

def check_version_endpoint():
    """
    Check if the /version endpoint is responding correctly
    """
    max_retries = 30
    retry_interval = 1

    for _ in range(max_retries):
        try:
            response = requests.get('http://localhost:8080/version')
            if response.status_code == 200:
                print(f"Version endpoint responded with: {response.text}")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(retry_interval)
        print("Waiting for service to be ready...")

    print("Service failed to respond correctly")
    return False

def run_command(command):
    """
    Run a shell command and return the result
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Exit code: {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def generate_dockerfile(workspace_dir):
    """
    Generate a basic Dockerfile that exposes port 8080 and uses the target repo's code
    """
    dockerfile_content = """FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "main.py"]
"""
    dockerfile_path = os.path.join(workspace_dir, "Dockerfile")
    try:
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        return True
    except Exception as e:
        print(f"Error generating Dockerfile: {e}")
        return False
def main():
    def check_required_files(workspace_dir):
        """
        Check if required files (main.py and requirements.txt) exist in the workspace
        """
        required_files = ['main.py', 'requirements.txt']
        missing_files = []

        for file in required_files:
            file_path = os.path.join(workspace_dir, file)
            if not os.path.isfile(file_path):
                missing_files.append(file)

        if missing_files:
            print(f"Error: Missing required files: {', '.join(missing_files)}")
            return False
        return True
    # Get the directory containing the Dockerfile
    workspace_dir = os.environ.get('GITHUB_WORKSPACE', os.getcwd())

    print("Starting smoke test...")
    # Check for required files
    print("Checking for required files...")
    if not check_required_files(workspace_dir):
        print("Smoke test failed: Missing required files")
        sys.exit(1)
    # Generate Dockerfile
    print("Generating Dockerfile...")
    if not generate_dockerfile(workspace_dir):
        print("Failed to generate Dockerfile")
        sys.exit(1)

    # Build the Docker image
    print("Building Docker image...")
    if not run_command(f"docker build -t smoke-test {workspace_dir}"):
        print("Failed to build Docker image")
        sys.exit(1)

    # Run the Docker container
    print("Running Docker container...")
    if not run_command("docker run --rm -d -p 8080:8080 smoke-test"):
        print("Failed to start container")
        sys.exit(1)

    # Check if the service responds correctly
    print("Testing /version endpoint...")
    if not check_version_endpoint():
        print("Version endpoint test failed")
        sys.exit(1)

    print("Smoke test completed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()
