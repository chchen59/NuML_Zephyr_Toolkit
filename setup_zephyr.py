import subprocess
import sys
import os

# Upgrade pip
Print('Upgrade pip...')
command = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
ret = subprocess.run(command)
if ret.returncode != 0:
    sys.exit(ret.returncode)

# Install the 'west' package using pip
Print('Install the west package...')
command = [sys.executable, "-m", "pip", "install", "west"]
ret = subprocess.run(command)
if ret.returncode != 0:
    sys.exit(ret.returncode)

# Initialize a workspace and retrieve repositories
print('Initialize a workspace and retrieve repositories...')
command = ["west", "init", "zephyrproject"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to initialize west workspace and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Change directory to the workspace
os.chdir("zephyrproject")

# Install external modules specified in the west manifest
print('Add tflite-micro module to west manifest...')
command = ["west", "config", "manifest.project-filter", "--", "+tflite-micro"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to initialize west manifest and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Update the workspace to fetch all repositories
print('Update the workspace to fetch all repositories...')
command = ["west", "update"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to update west workspace and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Export a Zephyr CMake package
print('Export Zephyr CMake package...')
command = ["west", "zephyr-export"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to export Zephyr package and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Install the Python dependencies
print('Install the west Python dependencies...')
command = ["cmd", "/c", "zephyr\\scripts\\utils\\west-packages-pip-install.cmd"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to install Zephyr Python dependencies and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Install zephyr sdk(toolchain)
print('Install arm-zephyr-eabi toolchain...')
command = ["west", "sdk", "install", "--version", "0.17.4", "-t", "arm-zephyr-eabi"]
ret = subprocess.run(command)
if ret.returncode != 0:
    print("Failed to install Zephyr SDK and retcode =", ret.returncode)
    sys.exit(ret.returncode)

# Reinstall pyocd from OpenNuvoton's GitHub repository
print('Reinstall pyocd from OpenNuvoton GitHub repository...')
command = [sys.executable, "-m", "pip", "uninstall", "pyocd", "-y"]
ret = subprocess.run(command)
if ret.returncode != 0:
    sys.exit(ret.returncode)

command = [sys.executable, "-m", "pip", "install", "git+https://github.com/OpenNuvoton/pyOCD"]
ret = subprocess.run(command)
if ret.returncode != 0:
    sys.exit(ret.returncode)

# Return to original directory
os.chdir("../")
print("Setup completed successfully.")
