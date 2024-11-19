import os
import subprocess
import time


def generate_smoke_test(project_folder):
    import os

    required_files = ['main.py', 'requirements.txt']
    missing_files = [f for f in required_files if not os.path.isfile(os.path.join(project_folder, f))]

    if missing_files:
        return (False, f"No file {missing_files[0]}")

    # Generate Dockerfile
    dockerfile_content = '''\
# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy requirement.txt first to leverage Docker cache
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the rest of the source code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Command to run your application
CMD ["python", "main.py"]
'''

    with open(os.path.join(project_folder, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)

    # Ensure .github/workflows directory exists
    workflows_dir = os.path.join(project_folder, '.github', 'workflows')
    os.makedirs(workflows_dir, exist_ok=True)

    # Generate main.yml
    main_yml_content = '''\
name: Smoke Test

on:
  push:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Build Docker image
      run: docker build -t myapp .

    - name: Run Docker container
      run: |
        docker run -d -p 5000:5000 --name myapp_container myapp
        sleep 5  # Wait for the service to start

    - name: Install curl
      run: sudo apt-get install -y curl

    - name: Test application
      run: |
        RESPONSE=$(curl -s http://localhost:5000)
        echo "Response: $RESPONSE"
        if [ -z "$RESPONSE" ]; then
          echo "No response from the application. Failing the test."
          exit 1
        fi

    - name: Stop and remove Docker container
      if: always()
      run: |
        docker stop myapp_container
        docker rm myapp_container
'''

    with open(os.path.join(workflows_dir, 'main.yml'), 'w') as f:
        f.write(main_yml_content)

    return (True, "Files generated successfully")


def local_tests(project_folder):
    old_cwd = os.getcwd()
    os.chdir(project_folder)
    try:
        print("Building Docker image locally...")
        result = subprocess.run(['docker', 'build', '-t', 'myapp_local', '.', '--progress', 'plain'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Failed to build Docker image.")
            print(result.stderr.decode('utf-8'))
            return (False, "Failed to build Docker image locally")

        # Run Docker container
        print("Running Docker container locally...")
        result = subprocess.run(['docker', 'run', '-d', '-p', '5000:5000', '--name', 'myapp_container_local', 'myapp_local'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Failed to run Docker container.")
            print(result.stderr.decode('utf-8'))
            return (False, "Failed to run Docker container locally")

        # Wait for the application to start
        time.sleep(5)

        # Test the application
        print("Testing the application locally...")
        try:
            import requests
        except ImportError:
            subprocess.check_call(['pip', 'install', 'requests'])
            import requests

        try:
            response = requests.get('http://localhost:5000')
            print(f"Response: {response.text}")
            if response.status_code != 200:
                print("Application returned non-200 status code.")
                return (False, "Application failed the local test")
        except Exception as e:
            print(f"Exception occurred: {e}")
            return (False, f"Failed to connect to the application locally: {e}")

    finally:
        # Cleanup
        print("Cleaning up Docker container locally...")
        subprocess.run(['docker', 'stop', 'myapp_container_local'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(['docker', 'rm', 'myapp_container_local'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.chdir(old_cwd)
