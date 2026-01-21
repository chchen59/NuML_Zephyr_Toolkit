import subprocess
import sys
import os

# Install the 'west' package using pip
command = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
ret = subprocess.run(command)
if ret.returncode != 0:
    sys.exit(ret.returncode)

# Initialize a workspace and retrieve repositories
command = ["west", "init", "zephyrproject"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to initialize west workspace and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Change directory to the workspace
os.chdir("zephyrproject")

# Install external modules specified in the west manifest
command = ["west", "config", "manifest.project-filter", "--", "+tflite-micro"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to initialize west manifest and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Update the workspace to fetch all repositories
command = ["west", "update"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to update west workspace and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Export a Zephyr CMake package
command = ["west", "zephyr-export"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to export Zephyr package and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Install the Python dependencies
command = ["cmd", "/c", "zephyr\\scripts\\utils\\west-packages-pip-install.cmd"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to install Zephyr Python dependencies and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Install zephyr sdk(toolchain)
command = ["west", "sdk", "install", "--version", "0.17.4", "-t", "arm-zephyr-eabi"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to install Zephyr SDK and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Return to original directory
os.chdir("../")
print("Setup completed successfully.")
