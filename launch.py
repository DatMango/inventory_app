import os
import subprocess
import platform

CONTAINER_NAME = "inventory"

def run_command(command):
    result = subprocess.run(command, shell=True,
                            capture_output=True, text=True)

    return result.returncode

# def container_exists():
#     return run_command(f"docker ps -a | findstr {CONTAINER_NAME}") == 0

# def container_running():
#     return run_command(f"docker ps | findstr {CONTAINER_NAME}") == 0

# logic for checking existence is by listing docker containers and ctrl+f-ing it 
def container_exists():
    command = f"docker ps -a | {'findstr' if platform.system() == 'Windows' else 'grep'} {CONTAINER_NAME}"
    print(platform.system())
    return run_command(command) == 0

def container_running():
    command = f"docker ps | {'findstr' if platform.system() == 'Windows' else 'grep'} {CONTAINER_NAME}"
    print(platform.system())
    return run_command(command) == 0

if not container_exists():
    print("Container does not exist. Building image and creating container...")
    run_command(f"docker build -t {CONTAINER_NAME} .")
    run_command(f"docker create --name {CONTAINER_NAME} -p 3000:3000 {CONTAINER_NAME}")

if not container_running():
    print("Starting container...")
    run_command(f"docker start {CONTAINER_NAME}")

print("Running app inside the container...")