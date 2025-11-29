import sys
import subprocess
import os

print(f"Python executable: {sys.executable}")

requirements_file = "requirements.txt"
if not os.path.exists(requirements_file):
    print(f"Error: {requirements_file} not found.")
    sys.exit(1)

try:
    print(f"Installing dependencies from {requirements_file}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    print("Installation successful")
except subprocess.CalledProcessError as e:
    print(f"Installation failed: {e}")
