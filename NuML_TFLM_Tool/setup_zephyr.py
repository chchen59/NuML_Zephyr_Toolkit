import subprocess
import sys

# Install the 'west' package using pip
subprocess.check_call([sys.executable, "-m", "pip", "install", "west"])

